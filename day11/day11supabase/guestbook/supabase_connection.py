"""config.json에서만 Supabase 연결 설정을 읽습니다."""

import json
from pathlib import Path

import psycopg
from psycopg.rows import dict_row


def connect_database(config_path: Path | None = None):
    path = Path(config_path) if config_path is not None else Path(__file__).with_name("config.json")
    if not path.is_file():
        raise RuntimeError("프로그램과 같은 폴더에 Supabase 접속 정보가 담긴 config.json을 준비해주세요.")
    config = json.loads(path.read_text(encoding="utf-8-sig"))
    database = config.get("dbname") or config.get("database")
    if not database or any(not config.get(key) for key in ("host", "user", "password")):
        raise RuntimeError("config.json의 host, user, password, dbname 항목을 확인해주세요.")
    return psycopg.connect(
        host=config["host"],
        port=config.get("port", 5432),
        dbname=database,
        user=config["user"],
        password=config["password"],
        sslmode="require",
        connect_timeout=10,
        row_factory=dict_row,
        prepare_threshold=None,
    )
