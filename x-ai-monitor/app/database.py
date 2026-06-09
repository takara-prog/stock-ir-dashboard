import os
import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(os.getenv("DB_PATH", "/data/tweets.db"))


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def _db():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS tweets (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id      TEXT UNIQUE NOT NULL,
                text          TEXT NOT NULL,
                likes         INTEGER DEFAULT 0,
                retweets      INTEGER DEFAULT 0,
                collected_date TEXT NOT NULL,
                author_id     TEXT DEFAULT '',
                created_at    TEXT DEFAULT '',
                raw_json      TEXT DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS analyses (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                analyzed_at  TEXT NOT NULL,
                period_start TEXT NOT NULL,
                period_end   TEXT NOT NULL,
                keyword      TEXT NOT NULL,
                result       TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS settings (
                key        TEXT PRIMARY KEY,
                value      TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """)


# ---- Settings ----

def get_setting(key: str, default: str = "") -> str:
    with _db() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    now = datetime.utcnow().isoformat()
    with _db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, ?)",
            (key, value, now),
        )


# ---- Tweets ----

def insert_tweet(
    tweet_id: str,
    text: str,
    likes: int,
    retweets: int,
    collected_date: str,
    author_id: str = "",
    created_at: str = "",
    raw_json: str = "",
) -> bool:
    with _db() as conn:
        cur = conn.execute(
            """INSERT OR IGNORE INTO tweets
               (tweet_id, text, likes, retweets, collected_date, author_id, created_at, raw_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (tweet_id, text, likes, retweets, collected_date, author_id, created_at, raw_json),
        )
        return cur.rowcount > 0


def get_tweets_last_7_days() -> list[dict]:
    with _db() as conn:
        rows = conn.execute(
            """SELECT * FROM tweets
               WHERE collected_date >= date('now', '-6 days')
               ORDER BY collected_date DESC, likes DESC"""
        ).fetchall()
        return [dict(r) for r in rows]


def get_tweets_by_date_range(start_date: str, end_date: str) -> list[dict]:
    with _db() as conn:
        rows = conn.execute(
            "SELECT * FROM tweets WHERE collected_date BETWEEN ? AND ? ORDER BY collected_date ASC",
            (start_date, end_date),
        ).fetchall()
        return [dict(r) for r in rows]


def get_collect_status() -> list[dict]:
    with _db() as conn:
        rows = conn.execute(
            """SELECT collected_date, COUNT(*) as count
               FROM tweets GROUP BY collected_date
               ORDER BY collected_date DESC LIMIT 14"""
        ).fetchall()
        return [dict(r) for r in rows]


# ---- Analyses ----

def insert_analysis(period_start: str, period_end: str, keyword: str, result: str) -> None:
    now = datetime.utcnow().isoformat()
    with _db() as conn:
        conn.execute(
            """INSERT INTO analyses (analyzed_at, period_start, period_end, keyword, result)
               VALUES (?, ?, ?, ?, ?)""",
            (now, period_start, period_end, keyword, result),
        )


def get_latest_analysis() -> dict | None:
    with _db() as conn:
        row = conn.execute(
            "SELECT * FROM analyses ORDER BY analyzed_at DESC LIMIT 1"
        ).fetchone()
        return dict(row) if row else None


def get_analyses_history(limit: int = 5) -> list[dict]:
    with _db() as conn:
        rows = conn.execute(
            "SELECT * FROM analyses ORDER BY analyzed_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
