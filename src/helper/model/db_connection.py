import sqlite3


def query_get_all(db: str, query: str) -> list[tuple[str, ...]]:
    cursor = get_cursor(db)
    result = cursor.execute(query).fetchall()
    return result


def query_get_one(db: str, query: str):
    cursor = get_cursor(db)
    result = cursor.execute(query).fetchone()
    return result


def get_cursor(db: str) -> sqlite3.Cursor:
    con = sqlite3.connect(db)
    return con.cursor()
