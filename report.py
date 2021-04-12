import sqlite3, os

conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "Chinook_Sqlite_AutoIncrementPKs.sqlite"))
cur = conn.cursor()
# Ansprechen der lokalen sqlite Datenbank
cur.execute(f"  SELECT  EmployeeId, LastName,   \
                        FirstName, Title,       \
                        ReportsTo               \
                from employee                   \
                        ;")

list_data = cur.fetchall()

for item in list_data:
    if item[4] == None:
        print(f"{item[1]} {item[2]}, {item[3]} reports to noone")
    else:
        print(f"{item[1]} {item[2]}, {item[3]} reports to {list_data[item[4]-1][3]}")
        