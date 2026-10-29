"""HTML 폼과 Supabase PostgreSQL 한 테이블로 만드는 방명록."""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import parse_qs

import psycopg
from fastapi import FastAPI, Query, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from supabase_connection import connect_database

BASE_DIR = Path(__file__).resolve().parent
PAGE_SIZE = 20
MAX_ENTRIES = 1000
MAX_BODY_BYTES = 16384
TEMPLATE = (BASE_DIR / "templates" / "index.html").read_text(encoding="utf-8")


class EntryInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=30)
    message: str = Field(min_length=1, max_length=1000)

    @field_validator("name", "message")
    @classmethod
    def reject_null_character(cls, value: str) -> str:
        if "\x00" in value:
            raise ValueError("null 문자는 입력할 수 없습니다.")
        return value


def connect(config_path: Path | None = None):
    return connect_database(config_path or BASE_DIR / "config.json")


def init_db(config_path: Path | None = None):
    with connect(config_path) as connection:
        # 전용 스키마를 사용하며 다른 실습의 users 테이블은 변경하지 않습니다.
        connection.execute("CREATE SCHEMA IF NOT EXISTS guestbook_app")
        connection.execute("""
            CREATE TABLE IF NOT EXISTS guestbook_app.entries (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL CHECK(length(name) BETWEEN 1 AND 30),
                message TEXT NOT NULL CHECK(length(message) BETWEEN 1 AND 1000),
                created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def render_page(config_path=None, page=1, error="", name="", message="", status=200):
    with connect(config_path) as connection:
        total = connection.execute("SELECT COUNT(*) AS total FROM guestbook_app.entries").fetchone()["total"]
        last_page = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        page = min(page, last_page)
        records = connection.execute(
            "SELECT id, name, message, created_at FROM guestbook_app.entries "
            "ORDER BY id DESC LIMIT %s OFFSET %s",
            (PAGE_SIZE, (page - 1) * PAGE_SIZE),
        ).fetchall()

    cards = []
    for record in records:
        # PostgreSQL의 TIMESTAMPTZ는 문자열이 아닌 datetime으로 반환됩니다.
        created_at = record["created_at"].astimezone(timezone.utc).isoformat(timespec="seconds")
        cards.append(
            '<article class="entry"><header>'
            f'<strong>{escape(record["name"])}</strong>'
            f'<time datetime="{escape(created_at)}">'
            f'{escape(created_at.replace("T", " ").replace("+00:00", " UTC"))}'
            '</time></header>'
            f'<p class="message">{escape(record["message"])}</p></article>'
        )
    if not cards:
        cards.append('<p class="empty">아직 남겨진 인사가 없어요. 첫 번째 인사를 남겨 주세요.</p>')

    navigation = []
    if page > 1:
        navigation.append(f'<a href="/?page={page - 1}">← 이전</a>')
    navigation.append(f'<span>{page} / {last_page}</span>')
    if page < last_page:
        navigation.append(f'<a href="/?page={page + 1}">다음 →</a>')

    values = {
        "total": str(total),
        "error": f'<p class="error" role="alert">{escape(error)}</p>' if error else "",
        "name": escape(name, quote=True), "message": escape(message),
        "entries": "".join(cards), "navigation": "".join(navigation),
    }
    parts = TEMPLATE.split("@@")
    html = "".join(values.get(part, part) if i % 2 else part for i, part in enumerate(parts))
    return HTMLResponse(html, status_code=status)


def save_entry(config_path, entry: EntryInput):
    with connect(config_path) as connection:
        # SQLite의 BEGIN IMMEDIATE를 PostgreSQL 테이블 잠금으로 대체합니다.
        # 조회는 허용하고 글 수 확인과 INSERT를 다른 쓰기로부터 보호합니다.
        connection.execute("LOCK TABLE guestbook_app.entries IN SHARE ROW EXCLUSIVE MODE")
        total = connection.execute("SELECT COUNT(*) AS total FROM guestbook_app.entries").fetchone()["total"]
        if total >= MAX_ENTRIES:
            return False
        connection.execute(
            "INSERT INTO guestbook_app.entries (name, message, created_at) VALUES (%s, %s, %s)",
            (entry.name, entry.message, datetime.now(timezone.utc)),
        )
    # 정상 종료 시 커밋, 예외 시 롤백하며 연결도 자동으로 닫습니다.
    return True


def submit_entry(config_path, body: bytes):
    name, message = "", ""
    try:
        fields = parse_qs(body.decode("utf-8"), keep_blank_values=True, max_num_fields=2, errors="strict")
        if set(fields) != {"name", "message"} or any(len(value) != 1 for value in fields.values()):
            raise ValueError("잘못된 폼")
        name, message = fields["name"][0], fields["message"][0]
        entry = EntryInput(name=name, message=message)
    except (ValueError, ValidationError):
        return render_page(
            config_path, error="이름은 1~30자, 내용은 1~1,000자로 입력해 주세요. 공백만 입력할 수 없습니다.",
            name=name, message=message, status=422,
        )
    if not save_entry(config_path, entry):
        return render_page(
            config_path, error="방명록이 가득 찼습니다. 지금은 새 글을 받을 수 없습니다.",
            name=name, message=message, status=409,
        )
    return RedirectResponse("/", status_code=303)


def create_app(config_path: Path | None = None):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await run_in_threadpool(init_db, config_path)
        yield

    application = FastAPI(title="작은 방명록", lifespan=lifespan, docs_url=None, redoc_url=None)

    @application.middleware("http")
    async def response_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; "
            "frame-ancestors 'none'; base-uri 'none'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        return response

    @application.exception_handler(psycopg.Error)
    async def database_error(request: Request, error: psycopg.Error):
        return HTMLResponse(
            '<!doctype html><html lang="ko"><meta charset="utf-8">'
            '<title>잠시 후 다시 시도해 주세요</title><h1>저장소에 연결할 수 없습니다.</h1>'
            '<p>잠시 후 다시 시도해 주세요.</p><a href="/">방명록으로 돌아가기</a></html>',
            status_code=503,
        )

    @application.get("/", response_class=HTMLResponse)
    def home(page: int = Query(default=1, ge=1, le=1000000)):
        return render_page(config_path, page=page)

    @application.post("/entries")
    async def create_entry(request: Request):
        if request.headers.get("sec-fetch-site") == "cross-site":
            return HTMLResponse("다른 사이트에서는 글을 작성할 수 없습니다.", status_code=403)
        content_type = request.headers.get("content-type", "").split(";")[0].strip().lower()
        if content_type != "application/x-www-form-urlencoded":
            return HTMLResponse("HTML 폼으로 작성해 주세요.", status_code=415)
        body = bytearray()
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > MAX_BODY_BYTES:
                return HTMLResponse("입력한 내용이 너무 큽니다.", status_code=413)
        return await run_in_threadpool(submit_entry, config_path, bytes(body))

    @application.get("/health")
    def health():
        with connect(config_path) as connection:
            connection.execute("SELECT id FROM guestbook_app.entries LIMIT 1").fetchone()
        return {"status": "ok"}

    return application


app = create_app()
