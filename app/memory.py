"""Trí nhớ: lưu tin nhắn và những điều đáng nhớ về người dùng trong SQLite."""
import re
import sqlite3
from datetime import date, datetime, timedelta
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
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                upto_id INTEGER NOT NULL,    -- đã tóm tắt hết tin nhắn có id <= số này
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            );
            CREATE TABLE IF NOT EXISTS followups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,       -- chuyện nên hỏi thăm lại, ví dụ "Chiều nay đi tập chân"
                done INTEGER NOT NULL DEFAULT 0,
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
    def add_message(self, role: str, content: str) -> int:
        cur = self.conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
        self.conn.commit()
        return cur.lastrowid

    def delete_message(self, msg_id: int) -> None:
        self.conn.execute("DELETE FROM messages WHERE id = ?", (msg_id,))
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

    # --- Tóm tắt chuyện cũ ---
    def latest_summary(self) -> tuple[str, int]:
        row = self.conn.execute("SELECT content, upto_id FROM summaries ORDER BY id DESC LIMIT 1").fetchone()
        return (row[0], row[1]) if row else ("", 0)

    def add_summary(self, content: str, upto_id: int) -> None:
        self.conn.execute("INSERT INTO summaries (content, upto_id) VALUES (?, ?)", (content, upto_id))
        self.conn.commit()

    def messages_to_summarize(self, keep_recent: int) -> list[dict]:
        """Tin nhắn cũ chưa được tóm tắt, không tính `keep_recent` tin gần nhất (vẫn gửi nguyên văn)."""
        _, upto = self.latest_summary()
        rows = self.conn.execute(
            """SELECT id, role, content FROM messages
               WHERE id > ? AND id NOT IN (SELECT id FROM messages ORDER BY id DESC LIMIT ?)
               ORDER BY id""",
            (upto, keep_recent),
        ).fetchall()
        return [{"id": i, "role": r, "content": c} for i, r, c in rows]

    def last_message_time(self) -> datetime | None:
        row = self.conn.execute("SELECT created_at FROM messages ORDER BY id DESC LIMIT 1").fetchone()
        return datetime.fromisoformat(row[0]) if row else None

    # --- Chuyện cần hỏi thăm ---
    def add_followups(self, items: list[str]) -> None:
        known = {self._key(f["content"]) for f in self.pending_followups(min_hours=0)}
        for item in items:
            item = re.sub(r"\s+", " ", item).strip()
            key = self._key(item)
            if key and key not in known:
                known.add(key)
                self.conn.execute("INSERT INTO followups (content) VALUES (?)", (item,))
        self.conn.commit()

    def pending_followups(self, min_hours: float = 3, max_days: float = 7) -> list[dict]:
        """Chuyện chưa hỏi thăm, đã qua ít nhất `min_hours` giờ (để không hỏi ngay trong lúc đang kể)
        và chưa quá `max_days` ngày (chuyện quá cũ thì thôi)."""
        now = datetime.now()
        newest = (now - timedelta(hours=min_hours)).strftime("%Y-%m-%d %H:%M:%S")
        oldest = (now - timedelta(days=max_days)).strftime("%Y-%m-%d %H:%M:%S")
        rows = self.conn.execute(
            """SELECT id, content, created_at FROM followups
               WHERE done = 0 AND created_at <= ? AND created_at >= ? ORDER BY id""",
            (newest, oldest),
        ).fetchall()
        return [{"id": i, "content": c, "created_at": t} for i, c, t in rows]

    def done_followups(self, items: list[str]) -> None:
        """Đánh dấu đã hỏi thăm (so theo dạng rút gọn như điều đáng nhớ)."""
        keys = {self._key(f) for f in items}
        rows = self.conn.execute("SELECT id, content FROM followups WHERE done = 0").fetchall()
        for i, c in rows:
            if self._key(c) in keys:
                self.conn.execute("UPDATE followups SET done = 1 WHERE id = ?", (i,))
        self.conn.commit()

    # --- Điều đáng nhớ ---
    @staticmethod
    def _key(fact: str) -> str:
        """Dạng rút gọn để so trùng: bỏ hoa/thường, khoảng trắng thừa, dấu chấm câu ở cuối."""
        return re.sub(r"\s+", " ", fact).strip().rstrip(".!;,").strip().lower()

    def add_facts(self, facts: list[str]) -> None:
        known = {self._key(f) for f in self.all_facts()}
        for f in facts:
            f = re.sub(r"\s+", " ", f).strip()
            key = self._key(f)
            if key and key not in known:
                known.add(key)
                self.conn.execute("INSERT OR IGNORE INTO facts (content) VALUES (?)", (f,))
        self.conn.commit()

    def forget_facts(self, facts: list[str]) -> None:
        """Xóa các điều đã lỗi thời (so theo dạng rút gọn, nên lệch hoa/thường vẫn xóa được)."""
        keys = {self._key(f) for f in facts}
        for f in self.all_facts():
            if self._key(f) in keys:
                self.conn.execute("DELETE FROM facts WHERE content = ?", (f,))
        self.conn.commit()

    def replace_facts(self, facts: list[str]) -> None:
        """Thay toàn bộ danh sách (dùng sau khi gộp)."""
        self.conn.execute("DELETE FROM facts")
        self.add_facts(facts)

    def all_facts(self) -> list[str]:
        return [r[0] for r in self.conn.execute("SELECT content FROM facts ORDER BY id")]

    def delete_fact(self, content: str) -> None:
        self.conn.execute("DELETE FROM facts WHERE content = ?", (content,))
        self.conn.commit()

    def clear_facts(self) -> None:
        self.conn.execute("DELETE FROM facts")
        self.conn.commit()
