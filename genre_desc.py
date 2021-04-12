import sqlite3, pprint, os #import der lib
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),"Chinook_Sqlite_AutoIncrementPKs.sqlite"))

cur = conn.cursor()
# Ansprechen der lokalen sqlite Datenbank
cur.execute(f"SELECT g.name,                                    \
		        (SELECT count(*) FROM Track AS t                \
			        WHERE g.GenreId = t.GenreId) AS Count_Genre \
            from Genre AS g                                     \
            order by Count_Genre DESC;")

list_data = cur.fetchall()
pprint.pprint(list_data)
conn.close() 
