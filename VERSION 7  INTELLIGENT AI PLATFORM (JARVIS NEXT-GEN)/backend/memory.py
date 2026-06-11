import sqlite3
import os
import json

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
                tool_used  TEXT,
                tool_args  TEXT
            )
        """)
        con.commit()


def save_interaction(user_input: str, response: str, tool_used: str = None, tool_args: dict = None):
    with _conn() as con:
        con.execute(
            "INSERT INTO memory (user_input, response, tool_used, tool_args) VALUES (?, ?, ?, ?)",
            (user_input, response, tool_used, json.dumps(tool_args) if tool_args else None)
        )
        con.commit()


def get_history(limit: int = 20) -> list:
    with _conn() as con:
        rows = con.execute(
            "SELECT id, timestamp, user_input, response, tool_used, tool_args "
            "FROM memory ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [
        {
            "id":       r[0],
            "time":     r[1],
            "input":    r[2],
            "response": r[3],
            "tool":     r[4],
            "args":     json.loads(r[5]) if r[5] else None
        }
        for r in rows
    ]


def get_conversation_context(turns: int = 10) -> list:
    """
    Returns the last N conversation turns as OpenAI message format
    so GPT has memory of what was said before.
    """
    with _conn() as con:
        rows = con.execute(
            "SELECT user_input, response FROM memory ORDER BY id DESC LIMIT ?",
            (turns,)
        ).fetchall()

    # Reverse so oldest first (chronological order for the prompt)
    messages = []
    for user_input, response in reversed(rows):
        messages.append({"role": "user",      "content": user_input})
        messages.append({"role": "assistant", "content": response or ""})
    return messages


def get_stats() -> dict:
    with _conn() as con:
        total = con.execute("SELECT COUNT(*) FROM memory").fetchone()[0]
        tools = con.execute(
            "SELECT tool_used, COUNT(*) FROM memory WHERE tool_used IS NOT NULL GROUP BY tool_used"
        ).fetchall()
    return {"total_interactions": total, "tool_usage": dict(tools)}


def clear_history():
    with _conn() as con:
        con.execute("DELETE FROM memory")
        con.commit()
    return "History cleared."
