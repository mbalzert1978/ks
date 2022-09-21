import argparse
import csv
import inspect
import sys

import peewee as pw

import model


class SQLiteDataBase:
    def __init__(self) -> None:
        self.get_model()

    def get_model(self) -> None:
        self.__models = {
            name: obj
            for name, obj in inspect.getmembers(model)
            if isinstance(obj, pw.ModelBase)
            and not name.startswith(("Sqlite", "BaseM", "Model"))
        }

    def connect(self) -> None:
        model.database.connect()

    def __str__(self) -> str:
        return "\n".join(list(self.__models))

    def __repr__(self) -> str:
        return str(list(self.__models))

    def show(self, table: str) -> str:
        return "\n".join(
            ", ".join(
                "{!s}={!r}".format(key, val) for (key, val) in row.items()
            )
            for row in self.get_table(table).select().dicts()
        )

    def get_table(self, tablename: str) -> pw.ModelBase:
        return self.__models.get(tablename, {"NotFound": None})

    def to_csv(self, filename: str, tablename: str, delimiter: str) -> None:
        table = self.get_table(tablename)
        header = list(table.select().dicts()[0].keys())
        with open(filename, "w") as csvfile:
            writer = csv.DictWriter(csvfile, header, delimiter=delimiter)
            for row in table.select().dicts():
                writer.writerow(row)


def create_parser(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        (
            "Use create_model first!\n"
            + "\tScript to open an SQLite database and "
            + "extract a table and storing it as an .csv file."
        )
    )
    subparser = parser.add_subparsers(dest="command", required=True)
    show = subparser.add_parser(
        "show",
        help="Command to ONLY show the table",
    )
    to_csv = subparser.add_parser(
        "csv",
        help="Command to extract the given table to an .csv file",
    )
    subparser.add_parser(
        "all",
        help="Show all available tables in the Database.",
    )
    to_csv.add_argument(
        "-d",
        "--delimiter",
        help="The delimiter to use for the .csv file. Default = ';'",
        default=";",
    )
    to_csv.add_argument(
        "-f",
        "--file",
        help="The name of the .csv file. Default = 'data.csv'",
        default="data.csv",
    )
    parser.add_argument(
        "-db",
        "--database",
        help=(
            "Name of the SQLitedatabase. Default"
            + " = Chinook_Sqlite_AutoIncrementPKs"
        ),
        required=True,
    )
    parser.add_argument(
        "-t",
        "--table",
        help="Name of the table you want to access. Default = Customer",
        default="Customer",
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    args = create_parser(sys.argv[1:])
    sql_db = SQLiteDataBase()
    sql_db.connect()
    if args.command == "show":
        print(sql_db.show(args.table))
    elif args.command == "csv":
        sql_db.to_csv(
            filename=args.file, tablename=args.table, delimiter=args.delimiter
        )
    elif args.command == "all":
        print(sql_db)
