import sqlite3
import csv
import os


def export_customer_to_csv():
    conn = sqlite3.connect(
        os.path.join(
            os.path.dirname(__file__), "Chinook_Sqlite_AutoIncrementPKs.sqlite"
        )
    )

    cur = conn.cursor()
    querry = """
    SELECT * FROM Customer;
    """
    cur.execute(querry)
    list_data = cur.fetchall()
    with open(
        os.path.join(os.path.dirname(__file__), "data.csv"),
        "w",
        encoding="utf-8",
    ) as f:
        writer = csv.writer(
            f, delimiter=";", lineterminator="\n", quoting=csv.QUOTE_NONNUMERIC
        )
        writer.writerows(list_data)
    conn.close()


export_customer_to_csv()
