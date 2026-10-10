"""Trí nhớ: lưu tin nhắn và những điều đáng nhớ về người dùng trong SQLite."""
import re
import sqlite3
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path


def khong_dau(text: str) -> str:
    """Chữ thường, bỏ dấu tiếng Việt, gộp khoảng trắng: "Đá  Bóng" → "da bong" (để tìm kiếm)."""
    text = text.lower().replace("đ", "d")
    text = "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
    return " ".join(text.split())


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
            CREATE TABLE IF NOT EXISTS usage (
                day TEXT NOT NULL,           -- YYYY-MM-DD
                kind TEXT NOT NULL,          -- 'chat', 'tom_tat', 'gop'
                calls INTEGER NOT NULL DEFAULT 0,
                input_tokens INTEGER NOT NULL DEFAULT 0,
                output_tokens INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (day, kind)
            );
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,       -- việc cần nhắc, ví dụ "Gọi điện cho mẹ"
                due_at TEXT NOT NULL,        -- "YYYY-MM-DD HH:MM" giờ máy tính
                done INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS special_days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT NOT NULL,           -- "MM-DD", lặp lại mỗi năm
                content TEXT NOT NULL,       -- ví dụ "Sinh nhật Tân"
                wished_year INTEGER NOT NULL DEFAULT 0  -- năm gần nhất Bơ đã chúc
            );
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,       -- việc cần làm, ví dụ "Mua sữa"
                done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                done_at TEXT
            );
            CREATE TABLE IF NOT EXISTS kv (
                key TEXT PRIMARY KEY,        -- cài đặt nhỏ, ví dụ tuần đã tổng kết
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL UNIQUE,
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            );
            """
        )
        # Bản cũ chưa có cột cảm xúc thì thêm vào (dữ liệu cũ giữ nguyên)
        cols = {r[1] for r in self.conn.execute("PRAGMA table_info(messages)")}
        if "cam_xuc" not in cols:
            self.conn.execute("ALTER TABLE messages ADD COLUMN cam_xuc TEXT")
        if "lap" not in {r[1] for r in self.conn.execute("PRAGMA table_info(reminders)")}:
            # lời nhắc lặp lại: '' = một lần, 'ngay' = mỗi ngày, 'tuan' = mỗi tuần
            self.conn.execute("ALTER TABLE reminders ADD COLUMN lap TEXT NOT NULL DEFAULT ''")
        if "ghim" not in cols:  # 1 = tin đã ghim (tin đáng nhớ)
            self.conn.execute("ALTER TABLE messages ADD COLUMN ghim INTEGER NOT NULL DEFAULT 0")
        if "tu_dong" not in cols:  # 1 = tin Bơ tự gửi theo giờ (lời nhắc), không tính là "đang nói chuyện"
            self.conn.execute("ALTER TABLE messages ADD COLUMN tu_dong INTEGER NOT NULL DEFAULT 0")
        if "nhac_truoc_year" not in {r[1] for r in self.conn.execute("PRAGMA table_info(special_days)")}:
            # năm gần nhất Bơ đã nhắc trước một ngày ("mai là sinh nhật mẹ đó")
            self.conn.execute("ALTER TABLE special_days ADD COLUMN nhac_truoc_year INTEGER NOT NULL DEFAULT 0")
        if "tam_trang" not in cols:  # tâm trạng người dùng lúc gửi tin (vui, buon, met...), Bơ đoán
            self.conn.execute("ALTER TABLE messages ADD COLUMN tam_trang TEXT")
        self.conn.commit()

    # --- Tin nhắn ---
    def add_message(self, role: str, content: str, cam_xuc: str | None = None, tu_dong: bool = False) -> int:
        cur = self.conn.execute(
            "INSERT INTO messages (role, content, cam_xuc, tu_dong) VALUES (?, ?, ?, ?)",
            (role, content, cam_xuc, int(tu_dong)),
        )
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

    def history_page(self, limit: int = 50, before_id: int | None = None) -> list[dict]:
        """Tin nhắn cho giao diện (có id và giờ), cũ → mới. `before_id` để tải thêm tin cũ hơn."""
        rows = self.conn.execute(
            "SELECT id, role, content, created_at, cam_xuc, ghim FROM messages WHERE id < ? ORDER BY id DESC LIMIT ?",
            (before_id if before_id else 2**62, limit),
        ).fetchall()
        return [
            {"id": i, "role": r, "content": c, "created_at": t, "cam_xuc": e, "ghim": bool(g)}
            for i, r, c, t, e, g in reversed(rows)
        ]

    def set_pinned(self, msg_id: int, pinned: bool) -> bool:
        """Ghim / bỏ ghim một tin. Trả False nếu không có tin đó."""
        cur = self.conn.execute("UPDATE messages SET ghim = ? WHERE id = ?", (int(pinned), msg_id))
        self.conn.commit()
        return cur.rowcount > 0

    def pinned_messages(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT id, role, content, created_at FROM messages WHERE ghim = 1 ORDER BY id DESC"
        ).fetchall()
        return [{"id": i, "role": r, "content": c, "created_at": t} for i, r, c, t in rows]

    def search_messages(self, query: str, limit: int = 30) -> list[dict]:
        """Tìm tin nhắn chứa `query`, mới nhất trước. Không phân biệt hoa/thường và có dấu/không dấu:
        gõ "da bong" vẫn ra "Đá bóng". Từ khóa quá ngắn (dưới 2 chữ) thì trả rỗng."""
        q = khong_dau(query)
        if len(q) < 2:
            return []
        out = []
        cur = self.conn.execute("SELECT id, role, content, created_at FROM messages ORDER BY id DESC")
        for i, r, c, t in cur:
            if q in khong_dau(c):
                out.append({"id": i, "role": r, "content": c, "created_at": t})
                if len(out) >= limit:
                    break
        return out

    def chat_as_text(self) -> str:
        """Toàn bộ trò chuyện thành chữ dễ đọc, chia theo ngày (để tải về đọc lại)."""
        lines, day = [], None
        for role, content, t in self.conn.execute("SELECT role, content, created_at FROM messages ORDER BY id"):
            t = t or ""
            if t[:10] != day:
                day = t[:10]
                d = f"{day[8:10]}/{day[5:7]}/{day[:4]}" if len(day) == 10 else "Không rõ ngày"
                lines += ["", f"===== {d} ====="] if lines else [f"===== {d} ====="]
            who = "Bạn" if role == "user" else "Bơ"
            lines.append(f"[{t[11:16]}] {who}: {content}")
        return "\n".join(lines) + "\n" if lines else "(Chưa có tin nhắn nào)\n"

    def stats(self, today: date | None = None) -> dict:
        """Bơ và bạn: quen từ ngày nào, bao nhiêu ngày, bao nhiêu tin, bao nhiêu ngày có nói chuyện."""
        today = today or date.today()
        first, total, days = self.conn.execute(
            "SELECT MIN(created_at), COUNT(*), COUNT(DISTINCT substr(created_at, 1, 10)) FROM messages WHERE tu_dong = 0"
        ).fetchone()
        try:
            first_day = date.fromisoformat(first[:10]) if first else None
        except ValueError:
            first_day = None
        return {
            "quen_tu": first_day.strftime("%d/%m/%Y") if first_day else None,
            "so_ngay_quen": (today - first_day).days + 1 if first_day else 0,
            "so_tin": total,
            "so_ngay_tro_chuyen": days,
            "so_dieu_nho": len(self.all_facts()),
        }

    # --- Tâm trạng ---
    def set_mood(self, msg_id: int, mood: str) -> None:
        self.conn.execute("UPDATE messages SET tam_trang = ? WHERE id = ? AND role = 'user'", (mood, msg_id))
        self.conn.commit()

    def moods_by_day(self, days: int = 7, today: date | None = None) -> list[dict]:
        """Tâm trạng nổi bật từng ngày (cũ → mới). Ngày có cả "bình thường" lẫn buồn/vui thì lấy cái
        không bình thường xuất hiện nhiều nhất (bằng nhau thì lấy cái gần nhất). Ngày không có tin: None."""
        today = today or date.today()
        start = today - timedelta(days=days - 1)
        rows = self.conn.execute(
            "SELECT substr(created_at, 1, 10), tam_trang FROM messages "
            "WHERE role = 'user' AND tam_trang IS NOT NULL AND tam_trang != '' AND created_at >= ? ORDER BY id",
            (start.isoformat(),),
        ).fetchall()
        per_day: dict[str, list[str]] = {}
        for d, m in rows:
            per_day.setdefault(d, []).append(m)
        out = []
        for i in range(days):
            d = (start + timedelta(days=i)).isoformat()
            moods = per_day.get(d, [])
            strong = [m for m in moods if m != "binh_thuong"]
            pick = None
            if strong:
                best = max(strong.count(m) for m in strong)
                pick = [m for m in strong if strong.count(m) == best][-1]
            elif moods:
                pick = "binh_thuong"
            out.append({"ngay": d, "tam_trang": pick})
        return out

    def low_mood(self, today: date | None = None, days: int = 3, min_days: int = 2) -> list[str]:
        """Trong `days` ngày gần đây có ít nhất `min_days` ngày tâm trạng nổi bật là buồn/mệt/lo/giận
        → trả các tâm trạng đó (cũ → mới, không lặp). Không thì (hoặc hôm nay đã vui lại) trả []."""
        recent = self.moods_by_day(days, today)
        if recent[-1]["tam_trang"] == "vui":
            return []  # hôm nay đã vui lại rồi thì thôi
        low = [d["tam_trang"] for d in recent if d["tam_trang"] in ("buon", "met", "lo", "gian")]
        if len(low) < min_days:
            return []
        return list(dict.fromkeys(low))

    def get_kv(self, key: str, default: str = "") -> str:
        row = self.conn.execute("SELECT value FROM kv WHERE key = ?", (key,)).fetchone()
        return row[0] if row else default

    def set_kv(self, key: str, value: str) -> None:
        self.conn.execute("INSERT INTO kv (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                          (key, value))
        self.conn.commit()

    def user_messages_since(self, since: datetime, limit: int = 60) -> list[dict]:
        """Tin của người dùng từ `since` tới nay (cũ → mới), tối đa `limit` tin gần nhất."""
        rows = self.conn.execute(
            "SELECT content, created_at FROM messages WHERE role = 'user' AND created_at >= ? ORDER BY id DESC LIMIT ?",
            (since.strftime("%Y-%m-%d %H:%M:%S"), limit),
        ).fetchall()
        return [{"content": c, "created_at": t} for c, t in reversed(rows)]

    def replies_today(self) -> int:
        today = date.today().isoformat()
        (n,) = self.conn.execute(
            "SELECT COUNT(*) FROM messages WHERE role='assistant' AND tu_dong = 0 AND created_at LIKE ?",
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
        """Lúc hai bên trò chuyện gần nhất (kể cả lời chào của Bơ; lời nhắc tự động thì không tính)."""
        row = self.conn.execute(
            "SELECT created_at FROM messages WHERE tu_dong = 0 AND created_at IS NOT NULL ORDER BY id DESC LIMIT 1"
        ).fetchone()
        try:
            return datetime.fromisoformat(row[0]) if row else None
        except (TypeError, ValueError):
            return None

    # --- Chi phí API ---
    def add_usage(self, kind: str, input_tokens: int, output_tokens: int) -> None:
        self.conn.execute(
            """INSERT INTO usage (day, kind, calls, input_tokens, output_tokens) VALUES (?, ?, 1, ?, ?)
               ON CONFLICT(day, kind) DO UPDATE SET calls = calls + 1,
                 input_tokens = input_tokens + excluded.input_tokens,
                 output_tokens = output_tokens + excluded.output_tokens""",
            (date.today().isoformat(), kind, input_tokens, output_tokens),
        )
        self.conn.commit()

    def usage_since(self, day: str) -> dict:
        """Tổng số câu gọi API và token từ ngày `day` (YYYY-MM-DD) tới nay."""
        row = self.conn.execute(
            "SELECT COALESCE(SUM(calls),0), COALESCE(SUM(input_tokens),0), COALESCE(SUM(output_tokens),0)"
            " FROM usage WHERE day >= ?",
            (day,),
        ).fetchone()
        return {"calls": row[0], "input_tokens": row[1], "output_tokens": row[2]}

    def usage_rows_since(self, day: str) -> list[dict]:
        """Chi tiết từng ngày × từng loại ('chat', 'tom_tat', 'gop') từ ngày `day`."""
        rows = self.conn.execute(
            "SELECT day, kind, calls, input_tokens, output_tokens FROM usage WHERE day >= ? ORDER BY day, kind", (day,)
        ).fetchall()
        return [{"day": d, "kind": k, "calls": c, "input_tokens": i, "output_tokens": o} for d, k, c, i, o in rows]

    # --- Lời nhắc theo giờ ---
    _LAP = {"ngay": timedelta(days=1), "tuan": timedelta(weeks=1)}

    @classmethod
    def _next_time(cls, luc: datetime, lap: str, now: datetime) -> datetime:
        """Lời nhắc lặp lại: dời tới lần kế tiếp sau `now` (bỏ qua các lần đã lỡ)."""
        step = cls._LAP[lap]
        if luc > now:
            return luc
        return luc + step * ((now - luc) // step + 1)

    def add_reminders(self, items: list[dict], now: datetime | None = None) -> int:
        """Thêm lời nhắc dạng {"luc": "YYYY-MM-DD HH:MM", "viec": "...", "lap": "ngay"|"tuan"|""}.
        Giờ sai thì bỏ. Nhắc một lần mà giờ đã qua thì bỏ; nhắc lặp lại thì dời tới lần kế tiếp."""
        now = now or datetime.now()
        added = 0
        for it in items:
            if not isinstance(it, dict):
                continue
            viec = re.sub(r"\s+", " ", str(it.get("viec", ""))).strip()
            lap = str(it.get("lap") or "").strip().lower()
            lap = lap if lap in self._LAP else ""
            try:
                luc = datetime.strptime(str(it.get("luc", "")).strip()[:16], "%Y-%m-%d %H:%M")
            except ValueError:
                continue
            if not viec:
                continue
            if lap:
                luc = self._next_time(luc, lap, now - timedelta(minutes=1))
            elif luc < now - timedelta(minutes=1):
                continue
            due = luc.strftime("%Y-%m-%d %H:%M")
            exists = self.conn.execute(
                "SELECT 1 FROM reminders WHERE done = 0 AND due_at = ? AND lower(content) = lower(?) AND lap = ?",
                (due, viec, lap),
            ).fetchone()
            if lap and not exists:  # lặp lại: cùng việc, cùng giờ (cùng thứ nếu mỗi tuần) là trùng, dù khác ngày
                for (other,) in self.conn.execute(
                    "SELECT due_at FROM reminders WHERE done = 0 AND lower(content) = lower(?) AND lap = ?", (viec, lap)
                ):
                    try:
                        o = datetime.strptime(other, "%Y-%m-%d %H:%M")
                    except ValueError:
                        continue
                    if o.time() == luc.time() and (lap == "ngay" or o.weekday() == luc.weekday()):
                        exists = True
                        break
            if not exists:
                self.conn.execute("INSERT INTO reminders (content, due_at, lap) VALUES (?, ?, ?)", (viec, due, lap))
                added += 1
        self.conn.commit()
        return added

    def upcoming_reminders(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT id, content, due_at, lap FROM reminders WHERE done = 0 ORDER BY due_at"
        ).fetchall()
        return [{"id": i, "viec": c, "luc": t, "lap": lap} for i, c, t, lap in rows]

    def pop_due_reminders(self, now: datetime | None = None) -> list[dict]:
        """Lấy các lời nhắc đã tới giờ và đánh dấu đã nhắc (mỗi lần chỉ báo một lần).
        Lời nhắc lặp lại thì dời sang lần kế tiếp thay vì xong hẳn."""
        now = now or datetime.now()
        now_s = now.strftime("%Y-%m-%d %H:%M")
        due = [r for r in self.upcoming_reminders() if r["luc"] <= now_s]
        for r in due:
            if r["lap"] in self._LAP:
                try:
                    nxt = self._next_time(datetime.strptime(r["luc"], "%Y-%m-%d %H:%M"), r["lap"], now)
                    self.conn.execute(
                        "UPDATE reminders SET due_at = ? WHERE id = ?", (nxt.strftime("%Y-%m-%d %H:%M"), r["id"])
                    )
                    continue
                except ValueError:
                    pass
            self.conn.execute("UPDATE reminders SET done = 1 WHERE id = ?", (r["id"],))
        self.conn.commit()
        return due

    def delete_reminder(self, reminder_id: int) -> None:
        self.conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        self.conn.commit()

    # --- Ngày đặc biệt (sinh nhật, kỷ niệm...) ---
    def add_special_days(self, items: list[dict]) -> int:
        """Thêm ngày dạng {"ngay": "DD/MM", "viec": "Sinh nhật Tân"}. Ngày sai hoặc trùng thì bỏ."""
        added = 0
        for it in items:
            if not isinstance(it, dict):
                continue
            viec = re.sub(r"\s+", " ", str(it.get("viec", ""))).strip()
            m = re.match(r"\s*(\d{1,2})\s*[/-]\s*(\d{1,2})", str(it.get("ngay", "")))
            if not viec or not m:
                continue
            d, mo = int(m.group(1)), int(m.group(2))
            try:
                date(2000, mo, d)  # năm nhuận, để 29/02 hợp lệ
            except ValueError:
                continue
            day = f"{mo:02d}-{d:02d}"
            exists = self.conn.execute(
                "SELECT 1 FROM special_days WHERE day = ? AND lower(content) = lower(?)", (day, viec)
            ).fetchone()
            if not exists:
                self.conn.execute("INSERT INTO special_days (day, content) VALUES (?, ?)", (day, viec))
                added += 1
        self.conn.commit()
        return added

    def special_days(self) -> list[dict]:
        rows = self.conn.execute("SELECT id, day, content FROM special_days ORDER BY day, id").fetchall()
        return [{"id": i, "ngay": f"{d[3:]}/{d[:2]}", "viec": c} for i, d, c in rows]

    def special_days_today(self, today: date | None = None, only_unwished: bool = True) -> list[dict]:
        """Ngày đặc biệt rơi vào hôm nay. 29/02 thì năm không nhuận tính vào 28/02."""
        today = today or date.today()
        days = [today.strftime("%m-%d")]
        if days[0] == "02-28":
            try:
                date(today.year, 2, 29)
            except ValueError:
                days.append("02-29")
        rows = self.conn.execute(
            f"SELECT id, content FROM special_days WHERE day IN ({','.join('?' * len(days))})"
            + (" AND wished_year < ?" if only_unwished else "") + " ORDER BY id",
            (*days, today.year) if only_unwished else days,
        ).fetchall()
        return [{"id": i, "viec": c} for i, c in rows]

    def special_days_tomorrow(self, today: date | None = None) -> list[dict]:
        """Ngày đặc biệt rơi vào NGÀY MAI mà năm đó Bơ chưa nhắc trước."""
        tomorrow = (today or date.today()) + timedelta(days=1)
        rows = self.special_days_today(tomorrow, only_unwished=False)
        if not rows:
            return []
        ids = [d["id"] for d in rows]
        done = {
            i for (i,) in self.conn.execute(
                f"SELECT id FROM special_days WHERE id IN ({','.join('?' * len(ids))}) AND nhac_truoc_year >= ?",
                (*ids, tomorrow.year),
            )
        }
        return [d for d in rows if d["id"] not in done]

    def mark_eve_reminded(self, ids: list[int], year: int) -> None:
        for i in ids:
            self.conn.execute("UPDATE special_days SET nhac_truoc_year = ? WHERE id = ?", (year, i))
        self.conn.commit()

    def mark_wished(self, ids: list[int], year: int | None = None) -> None:
        year = year or date.today().year
        for i in ids:
            self.conn.execute("UPDATE special_days SET wished_year = ? WHERE id = ?", (year, i))
        self.conn.commit()

    def delete_special_day(self, day_id: int) -> None:
        self.conn.execute("DELETE FROM special_days WHERE id = ?", (day_id,))
        self.conn.commit()

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

    # --- Việc cần làm ---
    TODO_MAX = 50  # tối đa việc chưa xong (tránh danh sách phình mãi)

    def add_todos(self, items: list[str]) -> int:
        """Thêm việc cần làm, bỏ qua việc trùng với việc chưa xong. Trả về số việc đã thêm."""
        known = {self._key(t["viec"]) for t in self.todos(include_done=False)}
        added = 0
        for item in items:
            item = re.sub(r"\s+", " ", str(item)).strip()[:200]
            key = self._key(item)
            if key and key not in known and len(known) < self.TODO_MAX:
                known.add(key)
                self.conn.execute("INSERT INTO todos (content) VALUES (?)", (item,))
                added += 1
        self.conn.commit()
        return added

    def done_todos(self, items: list[str]) -> None:
        """Đánh dấu xong theo nội dung (Bơ chép lại y nguyên việc trong danh sách)."""
        # Bơ có thể chép cả ghi chú "(ghi 4 ngày trước)" trong lời dặn → bỏ đi trước khi so
        keys = {self._key(re.sub(r"\s*\(ghi [^()]*\)\s*$", "", str(t))) for t in items}
        for i, c in self.conn.execute("SELECT id, content FROM todos WHERE done = 0").fetchall():
            if self._key(c) in keys:
                self.set_todo_done(i, True, commit=False)
        self.conn.commit()

    def set_todo_done(self, todo_id: int, done: bool, commit: bool = True) -> bool:
        """Đánh dấu xong / chưa xong. Bỏ đánh dấu mà đã có việc y hệt đang mở (hoặc danh sách đầy)
        thì báo ValueError, để danh sách không có hai việc trùng."""
        if not done:
            row = self.conn.execute("SELECT content, done FROM todos WHERE id = ?", (todo_id,)).fetchone()
            if row and row[1]:
                opened = [t["viec"] for t in self.todos(include_done=False)]
                if self._key(row[0]) in {self._key(t) for t in opened}:
                    raise ValueError("Việc này đang có trong danh sách rồi")
                if len(opened) >= self.TODO_MAX:
                    raise ValueError(f"Danh sách đã đủ {self.TODO_MAX} việc chưa xong")
        cur = self.conn.execute(
            "UPDATE todos SET done = ?, done_at = CASE WHEN ? THEN datetime('now', 'localtime') ELSE NULL END WHERE id = ?",
            (int(done), int(done), todo_id),
        )
        if commit:
            self.conn.commit()
        return cur.rowcount > 0

    def delete_todo(self, todo_id: int) -> None:
        self.conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        self.conn.commit()

    def todos(self, include_done: bool = True, done_days: int = 3) -> list[dict]:
        """Việc chưa xong (cũ → mới), rồi việc đã xong trong `done_days` ngày gần đây (mới xong trước).
        Việc xong lâu hơn thì tự dọn khỏi danh sách."""
        since = (datetime.now() - timedelta(days=done_days)).strftime("%Y-%m-%d %H:%M:%S")
        if self.conn.execute("DELETE FROM todos WHERE done = 1 AND (done_at IS NULL OR done_at < ?)", (since,)).rowcount:
            self.conn.commit()
        rows = self.conn.execute("SELECT id, content, 0, created_at FROM todos WHERE done = 0 ORDER BY id").fetchall()
        if include_done:
            rows += self.conn.execute(
                "SELECT id, content, 1, created_at FROM todos WHERE done = 1 ORDER BY done_at DESC, id DESC"
            ).fetchall()
        return [{"id": i, "viec": c, "xong": bool(d), "created_at": t} for i, c, d, t in rows]

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

    def update_fact(self, old: str, new: str) -> bool:
        """Sửa một điều (giữ nguyên vị trí). Điều mới trống hoặc trùng điều khác thì trả False, không đổi gì."""
        new = re.sub(r"\s+", " ", new).strip()
        if not new:
            return False
        others = {self._key(f) for f in self.all_facts() if f != old}
        if self._key(new) in others:
            return False
        cur = self.conn.execute("UPDATE facts SET content = ? WHERE content = ?", (new, old))
        self.conn.commit()
        return cur.rowcount > 0

    def delete_fact(self, content: str) -> None:
        self.conn.execute("DELETE FROM facts WHERE content = ?", (content,))
        self.conn.commit()

    def clear_facts(self) -> None:
        self.conn.execute("DELETE FROM facts")
        self.conn.commit()

    # --- Sao lưu / khôi phục ---
    _BACKUP_TABLES = {
        "messages": ("role", "content", "created_at", "cam_xuc", "tu_dong", "ghim", "tam_trang"),
        "summaries": ("content", "upto_id", "created_at"),
        "followups": ("content", "done", "created_at"),
        "facts": ("content", "created_at"),
        "reminders": ("content", "due_at", "done", "lap"),
        "special_days": ("day", "content", "wished_year", "nhac_truoc_year"),
        "todos": ("content", "done", "created_at", "done_at"),
    }

    def export_all(self) -> dict:
        """Toàn bộ trí nhớ thành một dict (để lưu ra file JSON)."""
        out: dict = {"phien_ban": 1}
        for table, cols in self._BACKUP_TABLES.items():
            id_col = "id, " if table == "messages" else ""
            rows = self.conn.execute(f"SELECT {id_col}{', '.join(cols)} FROM {table} ORDER BY id").fetchall()
            names = (("id",) if id_col else ()) + cols
            out[table] = [dict(zip(names, r)) for r in rows]
        return out

    def import_all(self, data: dict) -> None:
        """Thay toàn bộ trí nhớ bằng bản sao lưu. Bản lỗi thì báo ValueError và không đổi gì."""
        if not isinstance(data, dict) or data.get("phien_ban") != 1:
            raise ValueError("Không phải file sao lưu của Bơ")
        try:
            with self.conn:  # lỗi giữa chừng thì hoàn tác hết
                for table, cols in self._BACKUP_TABLES.items():
                    self.conn.execute(f"DELETE FROM {table}")
                    for row in data.get(table, []):
                        if not isinstance(row, dict):
                            raise TypeError("dòng không hợp lệ")
                        # cột thiếu thì để SQLite tự điền mặc định (giờ tạo, done = 0)
                        use = (("id",) if table == "messages" and "id" in row else ()) + tuple(
                            c for c in cols if c in row
                        )
                        self.conn.execute(
                            f"INSERT INTO {table} ({', '.join(use)}) VALUES ({', '.join('?' * len(use))})",
                            [row.get(c) for c in use],
                        )
        except (sqlite3.Error, AttributeError, TypeError) as e:
            raise ValueError(f"File sao lưu bị hỏng: {e}") from e
