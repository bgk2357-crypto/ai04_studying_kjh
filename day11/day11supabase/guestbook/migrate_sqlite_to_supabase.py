"""SQLite의 기존 글을 비어 있는 Supabase 방명록으로 한 번만 이전합니다."""

import argparse
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from main import EntryInput, MAX_ENTRIES, connect, init_db


def read_entries(path: Path):
    if not path.is_file():
        raise ValueError("이전할 SQLite 파일이 없습니다.")
    # 원본 파일을 실수로 새로 만들거나 수정하지 않도록 읽기 전용으로 엽니다.
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as source:
        rows = source.execute("SELECT id, name, message, created_at FROM entries ORDER BY id").fetchall()
    if len(rows) > MAX_ENTRIES:
        raise ValueError("1,000건을 초과합니다. 이전 범위를 먼저 정해주세요.")
    records = []
    for entry_id, name, message, created_at in rows:
        if not isinstance(entry_id, int) or entry_id <= 0:
            raise ValueError("양의 정수 ID만 이전할 수 있습니다.")
        entry = EntryInput(name=name, message=message)
        timestamp = datetime.fromisoformat(created_at)
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        records.append((entry_id, entry.name, entry.message, timestamp))
    return records


def migrate(records, config_path=None):
    init_db(config_path)
    with connect(config_path) as destination:
        destination.execute("LOCK TABLE guestbook_app.entries IN SHARE ROW EXCLUSIVE MODE")
        total = destination.execute("SELECT COUNT(*) AS total FROM guestbook_app.entries").fetchone()["total"]
        if total:
            raise ValueError("Supabase 방명록에 이미 글이 있어 이전을 중단했습니다. 기존 글을 삭제하거나 덮어쓰지 않습니다.")
        for record in records:
            destination.execute(
                "INSERT INTO guestbook_app.entries (id, name, message, created_at) "
                "OVERRIDING SYSTEM VALUE VALUES (%s, %s, %s, %s)", record,
            )
        if records:
            destination.execute(
                "SELECT setval(pg_get_serial_sequence('guestbook_app.entries', 'id'), %s, true)",
                (max(record[0] for record in records),),
            )
    return len(records)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sqlite_file", type=Path, help="기존 guestbook.db 경로")
    parser.add_argument("--dry-run", action="store_true", help="원본 형식·건수만 확인하고 Supabase에는 연결하지 않음")
    args = parser.parse_args()
    try:
        entries = read_entries(args.sqlite_file)
        if args.dry_run:
            print(f"이전 가능한 글: {len(entries)}건. Supabase에는 연결하지 않았습니다.")
        else:
            print(f"이전 완료: {migrate(entries)}건. SQLite 원본은 유지했습니다.")
    except ValueError as error:
        parser.exit(1, f"{error}\n")
