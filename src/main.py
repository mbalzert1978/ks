from src.factory.factories import CreateSelectTable
from src.sqlite.sqlitedatabase import SQLiteDataBase


def main(options, model) -> None:
    commands = {
        "select_all_table": CreateSelectTable.factor_method(options.table),
    }
    sql_db = SQLiteDataBase(commands, model)
    if options.csv and options.table:
        sql_db.write_csv(
            filename=options.table
            if not options.filename
            else options.filename,
            delimiter=options.delimiter,
        )
    elif options.table:
        print(sql_db.select_all_table())
    else:
        print(sql_db)
