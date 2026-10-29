"""실제 Supabase에 접속하지 않고 입력 처리와 HTML 렌더링을 확인합니다."""
import ast
import asyncio
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlencode, parse_qs, urlsplit
from html import escape

from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse, RedirectResponse

ROOT = Path(__file__).resolve().parent
tree = ast.parse((ROOT / "main.py").read_text(encoding="utf-8"))
names = {"render_page", "save_entry", "create_entry"}
functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names]
for node in functions:
    node.decorator_list = []


class Query:
    def __init__(self, database):
        self.database = database
        self.count_mode = False
    def select(self, columns, count=None):
        self.count_mode = count is not None
        return self
    def limit(self, value): return self
    def order(self, *args, **kwargs): return self
    def range(self, start, end):
        self.database.last_range = (start, end)
        return self
    def execute(self):
        return SimpleNamespace(count=len(self.database.rows), data=self.database.rows)


class Database:
    def __init__(self):
        self.rows = [{"id": 1, "name": "<script>", "message": "{{count}} & 인사", "created_at": "2026-10-29 11:28 KST"}]
        self.saved = []
        self.full = False
    def table(self, name):
        assert name == "entries"
        return Query(self)
    def rpc(self, name, params):
        assert name == "guestbook_add_entry"
        self.saved.append(params)
        return SimpleNamespace(execute=lambda: SimpleNamespace(data=not self.full))


class Request:
    def __init__(self, database, fields):
        self.app = SimpleNamespace(state=SimpleNamespace(database=database))
        self.headers = {"content-type": "application/x-www-form-urlencoded", "origin": "https://example.test"}
        self.url = SimpleNamespace(netloc="example.test", scheme="https")
        self.body = urlencode(fields).encode()
    async def stream(self):
        yield self.body


import tempfile
with tempfile.TemporaryDirectory() as directory:
    template_root = Path(directory)
    (template_root / "index.html").write_text("{{error}}{{name}}{{message}}{{count}}{{entries}}{{navigation}}", encoding="utf-8")
    scope = dict(BASE_DIR=template_root, PAGE_SIZE=20, MAX_BODY_BYTES=32768, escape=escape,
                 parse_qs=parse_qs, urlsplit=urlsplit, HTMLResponse=HTMLResponse,
                 RedirectResponse=RedirectResponse, run_in_threadpool=run_in_threadpool,
                 Request=Request)
    exec(compile(ast.Module(body=functions, type_ignores=[]), "main.py", "exec"), scope)
    database = Database()
    page = scope["render_page"](database, page=999)
    html = page.body.decode()
    assert "&lt;script&gt;" in html and "<script>" not in html
    assert "{{count}} &amp; 인사" in html
    assert database.last_range == (0, 19)

    async def verify():
        response = await scope["create_entry"](Request(database, {"name": " 홍길동 ", "message": " 안녕하세요 "}))
        assert response.status_code == 303
        assert database.saved[-1] == {"p_name": "홍길동", "p_message": "안녕하세요"}
        before = len(database.saved)
        response = await scope["create_entry"](Request(database, {"name": " ", "message": "인사"}))
        assert response.status_code == 422 and len(database.saved) == before
        database.full = True
        response = await scope["create_entry"](Request(database, {"name": "이름", "message": "인사"}))
        assert response.status_code == 409
        request = Request(database, {"name": "이름", "message": "인사"})
        request.headers["origin"] = "https://another.test"
        assert (await scope["create_entry"](request)).status_code == 403
    asyncio.run(verify())
print("PASS: escaping, template markers, pagination, save parameters, validation, full response, origin check")
