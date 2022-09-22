import csv
import inspect
import optparse
import string
import sys
from getpass import getpass
from optparse import OptionParser
from pathlib import Path

import peewee as pw

options: optparse.Values
args: list[str]


class SQLiteDataBase:
    def __init__(self, database: pw.SqliteDatabase) -> None:
        self.__db = database
        self.get_model()

    def get_model(self) -> None:
        self.__models = {
            name: obj
            for name, obj in inspect.getmembers(model)
            if isinstance(obj, pw.ModelBase)
            and not name.startswith(("Sqlite", "BaseM", "Model"))
        }

    def connect(self) -> None:
        self.__db.connect()

    def __str__(self) -> str:
        return "\n".join(list(self.__models))

    def __repr__(self) -> str:
        return str(list(self.__models))

    def show_table(self, table: str) -> str:
        return "\n".join(
            ", ".join(
                "{!s}={!r}".format(key, val) for (key, val) in row.items()
            )
            for row in self.get_table(table).select().dicts()
        )

    def get_table(self, tablename: str) -> pw.ModelBase:
        table = self.__models.get(tablename)
        if table:
            return table
        err("The table was not found in the database")
        sys.stdout.write(str(self))
        sys.exit(1)

    def write_to_csv(
        self, filename: str, tablename: str, delimiter: str
    ) -> None:
        filename = self.fix_file_extension(filename)
        table = self.get_table(tablename)
        header = self.extract_header(table)
        with open(filename, "w") as csvfile:
            writer = csv.DictWriter(csvfile, header, delimiter=delimiter)
            for row in table.select().dicts():
                writer.writerow(row)

    def extract_header(self, table: pw.ModelBase) -> list[str]:
        header = list(table.select().dicts()[0].keys())
        return header

    def fix_file_extension(self, filename: str) -> str:
        if not filename.endswith(".csv"):
            filename += ".csv"
        return filename


def err(msg) -> None:
    sys.stderr.write("\033[91m%s\033[0m\n" % msg)
    sys.stderr.flush()


def valid_filepath(s) -> bool:
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return all(c for c in s if c in valid_chars)


def get_option_parser() -> OptionParser:
    parser = OptionParser(usage="usage: %prog [options] database_name")
    ao = parser.add_option
    ao("-H", "--host", dest="host")
    ao("-p", "--port", dest="port", type="int")
    ao("-u", "--user", dest="user")
    ao("-P", "--password", dest="password", action="store_true")
    ao(
        "-t",
        "--table",
        dest="table",
        help="Name of the table you want to access.",
    )
    ao(
        "-d",
        "--delimiter",
        dest="delimiter",
        help="The delimiter to use for the .csv file. Default = ';'",
        default=";",
    )
    ao(
        "-f",
        "--filename",
        dest="filename",
        help="The filename to use for the .csv file."
        "Default = 'tablename.csv'",
        default=False,
    )
    ao(
        "-c",
        "--to-csv",
        action="store_true",
        dest="csv",
        help="Extract the given table to an .csv file",
    )
    return parser


def get_connect_kwargs(options):
    ops = ("host", "port", "user")
    kwargs = dict((o, getattr(options, o)) for o in ops if getattr(options, o))
    if options.password:
        kwargs["password"] = getpass()
    return kwargs


def check_model():
    return Path("model.py").is_file()


def main(options, sql_db: SQLiteDataBase) -> None:
    if options.csv and options.table:
        sql_db.write_to_csv(
            filename=options.table
            if not options.filename
            else options.filename,
            tablename=options.table,
            delimiter=options.delimiter,
        )
    elif options.table:
        sys.stdout.write(sql_db.show_table(options.table))
    else:
        sys.stdout.write(str(sql_db))


if __name__ == "__main__":
    raw_argv = sys.argv
    if not check_model():
        err("Missing required file 'model.py'.")
        sys.stdout.write("Use create_model.py to create a model.")
        sys.exit(1)
    import model

    parser = get_option_parser()
    options, args = parser.parse_args()
    if len(args) < 1:
        err('Missing required parameter "database".')
        parser.print_help()
        sys.exit(1)
    if len(options.delimiter) > 1:
        err('"delimiter" must be a 1-character string.')
        parser.print_help()
        sys.exit(1)
    if options.filename:
        if not valid_filepath(options.filename):
            err('"filename" must be a valid file/path.')
            parser.print_help()
            sys.exit(1)
    connect = get_connect_kwargs(options)
    database = args[-1]
    database = pw.SqliteDatabase(database, **connect)
    sql_db = SQLiteDataBase(database)
    sql_db.connect()
    main(options, sql_db)
