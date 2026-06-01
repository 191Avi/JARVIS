import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis.db")


def _conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp  TEXT    DEFAULT (datetime('now','localtime')),
                user_input TEXT    NOT NULL,
                response   TEXT,
                tool_used  TEXT
            )
        """)
        con.commit()


def save_interaction(user_input: str, response: str, tool_used: str = None):
    with _conn() as con:
        con.execute(
            "INSERT INTO memory (user_input, response, tool_used) VALUES (?, ?, ?)",
            (user_input, response, tool_used)
        )
        con.commit()


def get_history(limit: int = 20) -> list:
    with _conn() as con:
        rows = con.execute(
            "SELECT id, timestamp, user_input, response, tool_used "
            "FROM memory ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [
        {"id": r[0], "time": r[1], "input": r[2], "response": r[3], "tool": r[4]}
        for r in rows
    ]


def get_stats() -> dict:
    with _conn() as con:
        total = con.execute("SELECT COUNT(*) FROM memory").fetchone()[0]
        tools = con.execute(
            "SELECT tool_used, COUNT(*) FROM memory WHERE tool_used IS NOT NULL GROUP BY tool_used"
        ).fetchall()
    return {"total_interactions": total, "tool_usage": dict(tools)}
