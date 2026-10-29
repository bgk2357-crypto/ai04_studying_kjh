# Supabase 방명록

HTML 화면과 FastAPI를 유지하고, 저장소를 Supabase PostgreSQL로 변경했습니다.

- 실행 코드: `main.py`
- 설정: 이 폴더의 `config.json`에서만 읽음
- 저장 테이블: `guestbook_app.entries` 하나
- 원본 SQLite 코드: `main copy.py` (보관)
- 기존 글 이전: `migrate_sqlite_to_supabase.py` (직접 실행해야 이전됨)

## 시작하기

이 폴더에서 정상 Python 가상환경을 사용하세요.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

실행 전 Supabase의 **Connect → Session pooler**에서 확인한 host·port·user·DB 비밀번호를 `config.json`에 입력합니다. 형식은 `config.example.json`을 참고하세요. 실제 설정 파일은 GitHub에 올리지 않습니다.

주소: http://127.0.0.1:8000 / 연결 확인: http://127.0.0.1:8000/health

DB에 테이블을 만들기 전에 접속만 확인하려면 `python check_connection.py`를 실행합니다. 이 스크립트는 SELECT만 실행하며 글이나 테이블을 변경하지 않습니다. 공통 연결 코드는 `supabase_connection.py`에 있고, 연결 정보는 환경 변수가 아닌 config.json에서 읽습니다.

## 안내

전체 실행·Render 배포·연결 설정·기존 데이터 이전 절차는 [SUPABASE_GUIDE.md](SUPABASE_GUIDE.md)에 있습니다.

최초 실행 때 테이블을 생성합니다. 다른 실습의 users 테이블은 수정하지 않습니다. 기존 SQLite 파일의 글을 자동으로 이전하거나 삭제하지 않습니다.

이름 30자·내용 1,000자, 페이지당 20건, 최대 1,000건을 유지합니다. 입력 길이 검사·HTML 이스케이프·매개변수 SQL·트랜잭션을 적용했습니다.

## 테스트

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-supabase-dev.txt
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
```

`test_supabase.py`는 운영 접속 없이 PostgreSQL 연결 계약과 HTTP 동작을 검사합니다. `test_guestbook.py`는 보관한 원본 SQLite 코드의 회귀 테스트입니다. 테스트 통과는 실제 Supabase 연결 검증과 구분됩니다.

기존 SQLite 안내와 의존성 목록은 `README_SQLITE_ORIGINAL.md`, `requirements-sqlite-original.txt`에 보관했습니다.
