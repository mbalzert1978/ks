import sqlite3, csv, argparse #import der lib

parser = argparse.ArgumentParser()
parser.add_argument('--table', action='store',
                    dest='table_name',
                    help='Store a table')
table = parser.parse_args()

conn = sqlite3.connect("Chinook_Sqlite_AutoIncrementPKs.sqlite")

cur = conn.cursor()
# Ansprechen der lokalen sqlite Datenbank
cur.execute(f"SELECT * \
                    FROM \
                    {table.table_name} \
            ;")

data_csv = "data.csv"

list_data = cur.fetchall()
with open(data_csv, 'w', encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_NONNUMERIC)
    writer.writerows(list_data)
conn.close() 
