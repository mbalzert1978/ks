from pathlib import Path
import sqlite3


class Sq3LiteConnection:
    def __init__(self, db: str) -> None:
        if self._is_valid_db(db):
            self.db = db
        else:
            raise ValueError("No valid SQlite3 file.")
        self.cursor = self._get_cursor()

    def _get_cursor(self) -> sqlite3.Cursor:
        con = sqlite3.connect(self.db)
        return con.cursor()

    def _is_valid_db(self, value: str) -> bool:
        resolve = Path(value)
        db = resolve.resolve()
        if not db.is_file():
            return False
        with open(db, "rb") as fd:
            header = fd.read(100)
        return header[:16] == b"SQLite format 3\x00"

    def fetch_all(self, query: str) -> list[tuple[str, ...]]:
        return self.cursor.execute(query).fetchall()

    def fetch_one(self, query: str) -> tuple[str, ...]:
        return self.cursor.execute(query).fetchone()
