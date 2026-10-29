"""운영 Supabase에 접속하지 않는 HTTP·변환 계약 테스트."""

import json
import sqlite3
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock

import psycopg
from psycopg.rows import dict_row
import pytest
from fastapi.testclient import TestClient

import main
import migrate_sqlite_to_supabase as migration


class Result:
    def __init__(self, rows):
        self.rows = rows

    def fetchone(self):
        return self.rows[0] if self.rows else None

    def fetchall(self):
        return self.rows


class Connection:
    def __init__(self, state):
        self.state = state
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, error_type, error, traceback):
        self.closed = True
        self.state.exits.append(error_type)

    def execute(self, sql, parameters=None):
        self.state.calls.append((sql, parameters))
        compact = " ".join(sql.split())
        if compact.startswith(("CREATE SCHEMA", "CREATE TABLE", "LOCK TABLE")):
            return Result([])
        if compact.startswith("SELECT COUNT(*)"):
            return Result([{"total": len(self.state.records)}])
        if compact.startswith("SELECT id, name, message"):
            limit, offset = parameters
            return Result(list(reversed(self.state.records))[offset:offset + limit])
        if compact.startswith("SELECT id FROM"):
            return Result([{"id": 1}] if self.state.records else [])
        if compact.startswith("INSERT INTO"):
            assert "%s" in sql and "?" not in sql
            name, message, created_at = parameters
            self.state.records.append({"id": len(self.state.records) + 1, "name": name, "message": message, "created_at": created_at})
            return Result([])
        raise AssertionError(f"예상하지 않은 SQL: {compact}")


@pytest.fixture
def service(monkeypatch):
    state = SimpleNamespace(records=[], calls=[], exits=[], connections=[])

    def connect(database_url=None):
        connection = Connection(state)
        state.connections.append(connection)
        return connection

    monkeypatch.setattr(main, "connect", connect)
    with TestClient(main.create_app()) as client:
        yield client, state


def test_startup_and_health(service):
    client, state = service
    assert client.get("/").status_code == 200
    assert "아직 남겨진 인사" in client.get("/").text
    assert client.get("/health").json() == {"status": "ok"}
    assert any("TIMESTAMPTZ" in sql for sql, _ in state.calls)
    assert any("GENERATED ALWAYS AS IDENTITY" in sql for sql, _ in state.calls)
    assert all(connection.closed for connection in state.connections)


def test_save_and_datetime_rendering(service):
    client, state = service
    response = client.post("/entries", data={"name": "  방문자 ", "message": "안녕하세요\n반갑습니다"}, follow_redirects=False)
    assert response.status_code == 303
    assert state.records[0]["name"] == "방문자"
    assert isinstance(state.records[0]["created_at"], datetime)
    page = client.get("/").text
    assert "안녕하세요\n반갑습니다" in page
    assert " UTC" in page
    assert "총 1개의 인사" in page
    client.get("/")
    assert len(state.records) == 1


@pytest.mark.parametrize("data", [
    {"name": " ", "message": "인사"}, {"name": "이름", "message": " "},
    {"name": "가" * 31, "message": "인사"}, {"name": "이름", "message": "나" * 1001},
    {"name": "이름", "message": "\x00"}, {"name": "이름"},
    {"name": "이름", "message": "내용", "extra": "x"},
])
def test_validation(service, data):
    client, state = service
    assert client.post("/entries", data=data).status_code == 422
    assert state.records == []


def test_escaped_text_and_boundaries(service):
    client, state = service
    assert client.post("/entries", data={"name": "가" * 30, "message": "나" * 1000}).status_code == 200
    text = "<script>alert(1)</script> @@name@@ '; DROP TABLE entries; --"
    response = client.post("/entries", data={"name": '<b>"별명"</b>', "message": text})
    assert "<script>" not in response.text
    assert "&lt;script&gt;" in response.text
    assert "@@name@@" in response.text
    assert state.records[-1]["message"] == text


def test_table_lock_and_capacity(service, monkeypatch):
    client, state = service
    monkeypatch.setattr(main, "MAX_ENTRIES", 1)
    client.post("/entries", data={"name": "첫째", "message": "보존"})
    assert client.post("/entries", data={"name": "둘째", "message": "초과"}).status_code == 409
    assert len(state.records) == 1
    sqls = [sql for sql, _ in state.calls]
    lock = next(i for i, sql in enumerate(sqls) if sql.startswith("LOCK TABLE"))
    insert = next(i for i, sql in enumerate(sqls) if sql.startswith("INSERT INTO"))
    assert "SHARE ROW EXCLUSIVE MODE" in sqls[lock]
    assert lock < insert
    assert sqls[lock + 1].startswith("SELECT COUNT(*)")


def test_pagination(service):
    client, state = service
    for number in range(21):
        client.post("/entries", data={"name": "손님", "message": f"글-{number:02}"}, follow_redirects=False)
    page = client.get("/").text
    assert "글-20" in page and "글-00" not in page
    assert "글-00" in client.get("/?page=2").text
    assert "2 / 2" in client.get("/?page=9999").text
    assert client.get("/?page=0").status_code == 422


def test_protocol_and_safe_error(service, monkeypatch):
    client, _ = service
    assert client.post("/entries", json={"name": "a", "message": "b"}).status_code == 415
    assert client.post("/entries", content="x" * 16385, headers={"content-type": "application/x-www-form-urlencoded"}).status_code == 413
    assert client.post("/entries", data={"name": "a", "message": "b"}, headers={"sec-fetch-site": "cross-site"}).status_code == 403
    assert client.post("/entries", content="name=%FF&message=x", headers={"content-type": "application/x-www-form-urlencoded"}).status_code == 422
    monkeypatch.setattr(main, "connect", Mock(side_effect=psycopg.OperationalError("private-password-and-host")))
    response = client.get("/health")
    assert response.status_code == 503
    assert "private-password-and-host" not in response.text


def test_config_connection_options_ignore_database_url(monkeypatch, tmp_path):
    mocked = Mock()
    monkeypatch.setenv("DATABASE_URL", "postgresql://example.invalid/test")
    monkeypatch.setattr(main, "BASE_DIR", tmp_path)
    (tmp_path / "config.json").write_text(json.dumps({"host": "config.invalid", "dbname": "postgres", "user": "test", "password": "test"}), encoding="utf-8")
    monkeypatch.setattr(main.psycopg, "connect", mocked)
    main.connect()
    assert mocked.call_args.args == ()
    assert mocked.call_args.kwargs["host"] == "config.invalid"
    assert mocked.call_args.kwargs["sslmode"] == "require"
    assert mocked.call_args.kwargs["prepare_threshold"] is None
    assert mocked.call_args.kwargs["row_factory"] is dict_row


def test_config_fallback_without_reading_actual_credentials(monkeypatch, tmp_path):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(main, "BASE_DIR", tmp_path)
    mocked = Mock()
    monkeypatch.setattr(main.psycopg, "connect", mocked)
    with pytest.raises(RuntimeError, match="config.json"):
        main.connect()
    (tmp_path / "config.json").write_text(json.dumps({"host": "test.invalid", "port": 5432, "database": "postgres", "user": "test", "password": "test"}), encoding="utf-8")
    main.connect()
    assert mocked.call_args.kwargs["dbname"] == "postgres"
    assert mocked.call_args.kwargs["host"] == "test.invalid"


def test_migration_reads_source_without_modifying_it(tmp_path):
    path = tmp_path / "source.db"
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE entries(id INTEGER PRIMARY KEY, name TEXT, message TEXT, created_at TEXT)")
        connection.execute("INSERT INTO entries VALUES (8, '손님', '인사', '2026-10-28T00:00:00+00:00')")
    before = path.read_bytes()
    records = migration.read_entries(path)
    assert records[0][:3] == (8, "손님", "인사")
    assert records[0][3].tzinfo == timezone.utc
    assert path.read_bytes() == before


def test_migration_preserves_existing_destination(monkeypatch):
    connection = Mock()
    connection.__enter__ = Mock(return_value=connection)
    connection.__exit__ = Mock(return_value=False)
    connection.execute.return_value.fetchone.return_value = {"total": 1}
    monkeypatch.setattr(migration, "init_db", Mock())
    monkeypatch.setattr(migration, "connect", Mock(return_value=connection))
    with pytest.raises(ValueError, match="이미 글이 있어"):
        migration.migrate([])
    assert not any(call.args[0].startswith("INSERT") for call in connection.execute.call_args_list)
