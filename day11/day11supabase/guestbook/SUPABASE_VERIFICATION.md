# Supabase 변환 검증

2026-10-28 / Python 3.12.14 / FastAPI 0.115.12 / Pydantic 2.11.5 / Psycopg 3.3.6.

`pytest test_supabase.py test_guestbook.py -q -p no:cacheprovider` 결과: **32 passed, 1 warning**.

- Supabase 전환 코드: 연결 옵션(SSL·prepared statement 비활성화), JSON 설정 대체 경로, 초기 테이블 DDL, 생성 시각 datetime 표시, 입력 검증, HTML 이스케이프, 페이지 조회, 잠금 이후 건수 확인, 1,000건 상한 처리, 오류 시 접속 정보 비공개를 검증했습니다.
- 원본 SQLite 코드 회귀 테스트도 실행했습니다.
- 이전 도구는 원본 SQLite 파일을 수정하지 않는지와 이미 글이 있는 대상에는 INSERT하지 않는지를 확인했습니다.
- 테스트용 설정은 가짜 host·비밀번호를 사용했습니다. 실제 config.json의 내용은 읽거나 출력하지 않았습니다.

Supabase 테스트는 DB 접속을 대체한 단위 테스트입니다. 실제 PostgreSQL 서버에서 SQL 실행, 테이블 잠금 경합, Supabase 네트워크 연결, 운영 데이터 이전을 검증한 것은 아닙니다. 실제 연결은 사용자가 설정을 확인한 뒤 앱 시작과 `/health`로 확인해야 합니다.

SQLite 이전은 별도 명령으로만 수행합니다. 자동 테스트는 운영 DB에 접속하지 않으며 기존 DB 파일도 삭제하지 않습니다.

경고는 기존 Starlette 테스트 클라이언트의 AnyIO 폐기 예정 별칭 참조입니다. 테스트 실패는 아닙니다.

## config.json 전용 설정으로 변경

사용자 요청에 따라 DATABASE_URL 우선 처리를 제거했습니다. `supabase_connection.py`에서 config.json을 읽고 방명록·이전 도구·접속 확인 스크립트가 공통 연결을 사용합니다. 환경 변수에 다른 DB URL이 남아 있어도 파일 설정을 사용하는 테스트로 변경했고 32개 테스트가 다시 통과했습니다. 실제 비밀번호는 소스에 기록하지 않았으며 Supabase에 연결하거나 운영 데이터를 이전하지 않았습니다.

참고 자료:

- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://www.psycopg.org/psycopg3/docs/basic/usage.html#connection-context
- https://www.postgresql.org/docs/current/explicit-locking.html
