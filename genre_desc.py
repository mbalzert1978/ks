import sqlite3, argparse, pprint #import der lib

parser = argparse.ArgumentParser()
parser.add_argument('--table', action='store',
                    dest='table_name',
                    help='Store a table')
table = parser.parse_args()

conn = sqlite3.connect("Chinook_Sqlite_AutoIncrementPKs.sqlite")

cur = conn.cursor()
# Ansprechen der lokalen sqlite Datenbank
cur.execute(f"SELECT g.name,\
		        (SELECT count(*) FROM Track AS t \
			        WHERE g.GenreId = t.GenreId) AS Count_Genre \
            from Genre AS g \
            order by Count_Genre DESC;")

data_csv = "data.csv"

list_data = cur.fetchall()
pprint.pprint(list_data)
conn.close() 
