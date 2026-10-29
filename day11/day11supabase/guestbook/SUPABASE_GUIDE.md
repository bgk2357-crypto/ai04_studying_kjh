# SQLite 방명록을 Supabase로 바꾸기

변환 파일: `main.py`. 원본 SQLite 코드는 `main copy.py`에 보관했습니다. HTML 템플릿은 그대로 사용합니다. 회사 홈페이지의 Sites 코드와는 별도 프로젝트입니다.

## 1. 라이브러리 설치

이 폴더에서 정상적인 Python 환경으로 실행합니다. 실행 파일의 경로가 깨진 기존 가상환경이면 새 환경을 만드세요.

```powershell
cd C:\AI_04기\day11\day11supabase\guestbook
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-supabase.txt
```

기존 requirements.txt는 교육 환경의 버전 목록으로 보관했습니다. 새 방명록은 별도의 `requirements-supabase.txt`를 사용합니다.

## 2. Supabase 연결 정보

Supabase 프로젝트의 위쪽 **Connect**에서 Postgres 연결 정보를 확인합니다. 일반적인 IPv4 네트워크에서는 **Session pooler**를 선택하세요. host·port·user는 화면에 표시된 값을 그대로 사용합니다. Supabase API URL·API 키가 아니라 **데이터베이스 접속 정보와 DB 비밀번호**를 사용합니다.

공식 연결 안내: https://supabase.com/docs/guides/database/connecting-to-postgres

로컬에서는 현재 `config.json`을 그대로 읽습니다. 프로그램이 사용하는 키는 다음과 같습니다. `config.example.json`은 예시이며 실제 비밀번호가 없습니다.

```json
{
  "host": "Connect 화면의 host",
  "port": 5432,
  "dbname": "postgres",
  "user": "Connect 화면의 user",
  "password": "본인의 DB 비밀번호"
}
```

`dbname` 대신 기존 실습의 `database` 키도 지원합니다. DB 비밀번호를 변경하면 이 파일도 수정합니다. 설정 파일의 실제 값은 작업 중 출력하지 않았고 수정하지도 않았습니다. `config.json`은 GitHub에 올리지 않습니다. 이미 추적 중인 비밀번호 파일은 `.gitignore`를 추가해도 추적이 자동 해제되지 않으므로 업로드 목록을 확인하세요.

요청에 맞춰 연결 정보는 **config.json에서만** 읽습니다. 기존 DATABASE_URL 환경 변수가 남아 있어도 사용하지 않습니다. JSON의 password 값에는 DB 비밀번호를 그대로 입력합니다. 비밀번호와 설정 파일을 채팅이나 공개 저장소에 올리지 마세요.

## 3. 실행

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

첫 실행 때 DB에 접속하여 전용 스키마 `guestbook_app`과 테이블 `entries`를 만듭니다. Supabase Table Editor에서는 스키마를 **guestbook_app**으로 선택해 확인합니다. 다른 실습의 `users` 테이블은 건드리지 않습니다.

브라우저: http://127.0.0.1:8000

연결 확인: http://127.0.0.1:8000/health

접속이 실패하면 host·user·port·DB 비밀번호, 프로젝트 활성 상태와 네트워크를 확인합니다. 로컬 SQLite로 자동 대체하지 않습니다. 초기 DB 연결이 실패하면 앱 시작도 실패합니다.

## 4. 바뀐 부분

| SQLite | Supabase PostgreSQL |
|---|---|
| sqlite3.connect(파일) | psycopg.connect(접속 정보), SSL 필수 |
| sqlite3.Row | psycopg.rows.dict_row |
| INTEGER PRIMARY KEY | BIGINT GENERATED ALWAYS AS IDENTITY |
| created_at TEXT | created_at TIMESTAMPTZ |
| 값 자리표시자 `?` | 값 자리표시자 `%s` |
| BEGIN IMMEDIATE | 트랜잭션 안에서 테이블 쓰기 잠금 |
| 로컬 파일 entries | 원격 DB guestbook_app.entries |

DB 연결의 `with` 안에서 입력과 조회를 끝냅니다. 정상 종료하면 커밋하고, 오류가 나면 롤백하며 연결을 닫습니다. 이름·글 길이, 최신순, 20건 페이지, 1,000건 상한, HTML 이스케이프, POST 후 303 이동을 유지했습니다. 테이블 잠금으로 여러 앱 프로세스의 동시 등록도 직렬화합니다. 다른 클라이언트가 상한 검증을 우회해 DB에 직접 넣는 것까지 막는 제약은 아닙니다.

공식 Psycopg 설명: https://www.psycopg.org/psycopg3/docs/basic/usage.html#connection-context

## 5. SQLite에 남아 있는 글을 이전하려면

코드를 바꾸는 것만으로 기존 SQLite 데이터가 Supabase로 옮겨지지는 않습니다. 웹 서버를 중지하고 DB 파일을 백업한 뒤 아래 순서로 실행합니다.

```powershell
# 1. 원본 형식·건수 검사. Supabase에는 접속하지 않습니다.
.\.venv\Scripts\python.exe migrate_sqlite_to_supabase.py data\guestbook.db --dry-run

# 2. 연결 설정과 백업을 확인한 뒤 실제 이전
.\.venv\Scripts\python.exe migrate_sqlite_to_supabase.py data\guestbook.db
```

대상은 비어 있는 Supabase 방명록이어야 합니다. 글이 있으면 중단하므로 중복 입력·임의 덮어쓰기를 하지 않습니다. 기존 ID와 시각을 유지하고, 이후 새 글의 ID도 이어집니다. 타임존 없는 기존 시각은 원본 앱 기준 UTC로 해석합니다. SQLite 파일은 읽기 전용으로 열며 삭제하지 않습니다. 이미 유실된 서버의 SQLite 파일은 이 도구로 복구할 수 없습니다.

이번 작업 중에는 실제 Supabase 접속, 테이블 생성 또는 운영 글 이전을 실행하지 않았습니다.

## 6. Render 사용 시

이 방명록은 Python/FastAPI 앱입니다. 회사 홈페이지의 Node.js 설정과 구분합니다.

- Runtime: Python
- Root Directory: 이 폴더를 GitHub 맨 위에 올렸다면 비워두기. 저장소 전체라면 `day11/day11supabase/guestbook`.
- Build Command: `pip install -r requirements-supabase.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Secret Files: `config.json` 이름으로 본인의 설정 파일을 비공개 등록. GitHub에는 업로드하지 않음.
- Secret Files 사용 시 Start Command: `cp /etc/secrets/config.json ./config.json && uvicorn main:app --host 0.0.0.0 --port $PORT`
- 업로드: `main.py`, `supabase_connection.py`, `templates/index.html`, `requirements-supabase.txt`, `.gitignore`
- 업로드 제외: `config.json`, `.venv`, `data`, 비밀번호가 담긴 파일

글은 Render 파일이 아닌 Supabase DB에 저장됩니다. Supabase 프로젝트 자체가 일시 정지되거나 사용 한도에 도달하면 접속이 제한될 수 있습니다. 데이터 보존과 별도로 백업도 관리하세요.
