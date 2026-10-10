"""Trí nhớ: lưu tin nhắn và những điều đáng nhớ về người dùng trong SQLite."""
import sqlite3
from datetime import date
from pathlib import Path


class Memory:
    def __init__(self, db_path: Path):
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,          -- 'user' hoặc 'assistant'
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            );
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL UNIQUE,
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            );
            """
        )
        self.conn.commit()

    # --- Tin nhắn ---
    def add_message(self, role: str, content: str) -> None:
        self.conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
        self.conn.commit()

    def recent_messages(self, limit: int) -> list[dict]:
        rows = self.conn.execute(
            "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [{"role": r, "content": c} for r, c in reversed(rows)]

    def replies_today(self) -> int:
        today = date.today().isoformat()
        (n,) = self.conn.execute(
            "SELECT COUNT(*) FROM messages WHERE role='assistant' AND created_at LIKE ?",
            (today + "%",),
        ).fetchone()
        return n

    # --- Điều đáng nhớ ---
    def add_facts(self, facts: list[str]) -> None:
        for f in facts:
            f = f.strip()
            if f:
                self.conn.execute("INSERT OR IGNORE INTO facts (content) VALUES (?)", (f,))
        self.conn.commit()

    def all_facts(self) -> list[str]:
        return [r[0] for r in self.conn.execute("SELECT content FROM facts ORDER BY id")]

    def delete_fact(self, content: str) -> None:
        self.conn.execute("DELETE FROM facts WHERE content = ?", (content,))
        self.conn.commit()
