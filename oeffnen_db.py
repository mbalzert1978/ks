import sqlite3, csv, argparse #import der lib

parser = argparse.ArgumentParser()
parser.add_argument('--db', action='store',
                    dest='database_',
                    help='Stores a db_name', default="Chinook_Sqlite_AutoIncrementPKs.sqlite")
parser.add_argument('--table', action='store',
                    dest='table_name',
                    help='Stores a table', default="Customer")
parser.add_argument('--delimiter', action='store',
                    dest='delimiter_',
                    help='Stores a delimiter', default=";")
table = parser.parse_args()

def table_to_csv(db = "Chinook_Sqlite_AutoIncrementPKs.sqlite", table = "Customer", delimiter = ";"):
    conn = sqlite3.connect(f"{db}")
    cur = conn.cursor()
    # Ansprechen der lokalen sqlite Datenbank
    cur.execute(f"SELECT * \
                        FROM \
                        {table} \
                ;")
    data_csv = f"{table}.csv"
    list_data = cur.fetchall()
    with open(data_csv, 'w', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=delimiter, lineterminator="\n", quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(list_data)
    conn.close() 
    
    
table_to_csv(table.database_, table.table_name, table.delimiter_)
