"""SQLite database module for schedule data."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_db_path() -> Path:
    """Get the database path from env var or default."""
    import os
    return Path(os.environ.get("SCHEDULE_DB_PATH", "data/schedule.db"))


def init_db(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Initialize the database and return a connection."""
    if db_path is None:
        db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            "group" TEXT NOT NULL DEFAULT 'b25-cse-05',
            day TEXT NOT NULL,
            time_start TEXT NOT NULL,
            time_end TEXT NOT NULL,
            subject TEXT NOT NULL,
            room TEXT,
            teacher TEXT,
            week_type TEXT DEFAULT 'both',
            synced_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    return conn


def clear_lessons(conn: sqlite3.Connection, group: Optional[str] = None) -> int:
    """Delete lessons and return the count of deleted rows.
    If group is provided, only delete that group's lessons.
    """
    if group:
        cursor = conn.execute('DELETE FROM lessons WHERE "group" = ?', (group,))
    else:
        cursor = conn.execute("DELETE FROM lessons")
    conn.commit()
    return cursor.rowcount


def insert_lessons(conn: sqlite3.Connection, lessons: list[dict]) -> int:
    """Insert multiple lessons and return the count."""
    conn.executemany("""
        INSERT INTO lessons ("group", day, time_start, time_end, subject, room, teacher, week_type, synced_at)
        VALUES (:group, :day, :time_start, :time_end, :subject, :room, :teacher, :week_type, :synced_at)
    """, lessons)
    conn.commit()
    return len(lessons)


def get_now(conn: sqlite3.Connection, group: str = "b25-cse-05") -> Optional[dict]:
    """Get the current lesson based on system time and day of week."""
    import zoneinfo
    msk = zoneinfo.ZoneInfo("Europe/Moscow")
    now = datetime.now(msk)
    day_map = {
        0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"
    }
    today_ru = day_map.get(now.weekday(), "")
    current_minutes = now.hour * 60 + now.minute

    # Determine week type (even/odd ISO week number)
    iso_week = now.isocalendar()[1]
    week_type = "even" if iso_week % 2 == 0 else "odd"

    cursor = conn.execute("""
        SELECT * FROM lessons
        WHERE "group" = ? AND day = ?
          AND (week_type = ? OR week_type = 'both')
        ORDER BY time_start
    """, (group, today_ru, week_type))

    for row in cursor.fetchall():
        start_h, start_m = map(int, row["time_start"].split(":"))
        end_h, end_m = map(int, row["time_end"].split(":"))
        start_min = start_h * 60 + start_m
        end_min = end_h * 60 + end_m

        if start_min <= current_minutes <= end_min:
            return dict(row)

    return None


def get_schedule(conn: sqlite3.Connection, day: str, group: str = "b25-cse-05", week_type: Optional[str] = None) -> list[dict]:
    """Get all lessons for a specific day and group."""
    if week_type and week_type != "both":
        cursor = conn.execute("""
            SELECT * FROM lessons
            WHERE "group" = ? AND day = ? AND (week_type = ? OR week_type = 'both')
            ORDER BY time_start
        """, (group, day, week_type))
    else:
        cursor = conn.execute("""
            SELECT * FROM lessons
            WHERE "group" = ? AND day = ?
            ORDER BY time_start
        """, (group, day))

    return [dict(row) for row in cursor.fetchall()]


def get_room(conn: sqlite3.Connection, subject: str, group: str = "b25-cse-05") -> Optional[dict]:
    """Get the room for a subject."""
    cursor = conn.execute("""
        SELECT subject, room, teacher FROM lessons
        WHERE "group" = ? AND LOWER(subject) LIKE LOWER(?)
        LIMIT 1
    """, (group, f"%{subject}%"))
    row = cursor.fetchone()
    return dict(row) if row else None


def get_teacher(conn: sqlite3.Connection, subject: str, group: str = "b25-cse-05") -> Optional[dict]:
    """Get the teacher for a subject."""
    cursor = conn.execute("""
        SELECT subject, teacher, room FROM lessons
        WHERE "group" = ? AND LOWER(subject) LIKE LOWER(?)
        LIMIT 1
    """, (group, f"%{subject}%"))
    row = cursor.fetchone()
    return dict(row) if row else None


def get_week(conn: sqlite3.Connection, group: str = "b25-cse-05", week_type: Optional[str] = None) -> dict:
    """Get the full week schedule grouped by day."""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    schedule = {}

    for day in days:
        if week_type and week_type != "both":
            cursor = conn.execute("""
                SELECT * FROM lessons
                WHERE "group" = ? AND day = ? AND (week_type = ? OR week_type = 'both')
                ORDER BY time_start
            """, (group, day, week_type))
        else:
            cursor = conn.execute("""
                SELECT * FROM lessons
                WHERE "group" = ? AND day = ?
                ORDER BY time_start
            """, (group, day))

        lessons = [dict(row) for row in cursor.fetchall()]
        if lessons:
            schedule[day] = lessons

    return schedule


def get_last_sync(conn: sqlite3.Connection) -> Optional[str]:
    """Get the last sync timestamp."""
    cursor = conn.execute("SELECT MAX(synced_at) as last_sync FROM lessons")
    row = cursor.fetchone()
    return row["last_sync"] if row else None
