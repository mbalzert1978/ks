import sqlite3, os  # import der lib


def show_tables():
    conn = sqlite3.connect(
        os.path.join(
            os.path.dirname(__file__), "Chinook_Sqlite_AutoIncrementPKs.sqlite"
        )
    )
    cur = conn.cursor()
    # Ansprechen der lokalen sqlite Datenbank
    querry = """
    SELECT name FROM sqlite_master\
         WHERE type ='table' AND name NOT LIKE 'sqlite_%';
    """
    cur.execute(querry)
    return_value = cur.fetchall()
    conn.close()
    return return_value


print(show_tables())
