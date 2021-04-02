import sqlite3 #import der lib


def show_tables():
    conn = sqlite3.connect("Chinook_Sqlite_AutoIncrementPKs.sqlite")

    cur = conn.cursor()
    # Ansprechen der lokalen sqlite Datenbank
    cur.execute("SELECT name \
                        FROM \
                        sqlite_master \
                        WHERE \
                        type ='table' AND \
                        name NOT LIKE 'sqlite_%';")
    return cur.fetchall()
    conn.close() 
print(show_tables())
