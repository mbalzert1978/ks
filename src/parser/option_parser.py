import argparse
from optparse import OptionParser
from pathlib import Path


def get_option_parser(main: bool) -> OptionParser:
    usage = "usage: %prog [options] "
    parser = OptionParser()
    ao = parser.add_option
    if main:
        parser.usage = usage
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
            "--csv",
            action="store_true",
            dest="csv",
            help="Extract the given table to an .csv file",
        )
        return parser
    parser.usage = usage + "database_name"
    ao("-H", "--host", dest="host")
    ao("-p", "--port", dest="port", type="int")
    ao("-u", "--user", dest="user")
    ao("-P", "--password", dest="password", action="store_true")
    return parser


def get_main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    ap = parser.add_argument
    ap(
        dest="database",
        help="Filename of the database you want to access.",
        type=Path,
    )
    ap(
        "-t",
        "--table",
        dest="table",
        help="Name of the table you want to access.",
    )
    ap(
        "-d",
        "--delimiter",
        dest="delimiter",
        help="The delimiter to use for the output.csv file. Default = ';'",
        default=";",
    )
    ap(
        "-f",
        "--filename",
        dest="filename",
        help="The filename to use for the output.csv file."
        "Default = 'tablename.csv'",
        default=False,
    )
    ap(
        "-c",
        "--csv",
        action="store_true",
        dest="csv",
        help="Extract the given table to an .csv file",
    )
    return parser


def get_create_model_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    ap = parser.add_argument
    ap(
        dest="database",
        help="Filename of the database you want to access.",
        type=Path,
    )
    return parser
