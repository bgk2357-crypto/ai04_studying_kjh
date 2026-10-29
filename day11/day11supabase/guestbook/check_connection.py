"""설정 파일로 Supabase 접속 여부만 확인합니다. 테이블과 글은 변경하지 않습니다."""

import psycopg

from supabase_connection import connect_database


def main():
    try:
        with connect_database() as conn:
            result = conn.execute(
                "SELECT current_database() AS database_name, current_user AS user_name"
            ).fetchone()
            print("접속 성공")
            print(f"데이터베이스: {result['database_name']}")
            print(f"사용자: {result['user_name']}")
        print("접속 종료")
    except psycopg.Error:
        raise SystemExit("접속 실패: config.json의 host·port·user·DB 비밀번호와 프로젝트 활성 상태를 확인해주세요.")


if __name__ == "__main__":
    main()
