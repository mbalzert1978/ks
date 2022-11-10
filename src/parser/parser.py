import argparse
from pathlib import Path


def get_main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    ap = parser.add_argument
    ap(
        dest="database",
        help="URI of the database you want to access.",
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
        help="Filename of the SQlite3 database you want to access.",
        type=Path,
    )
    return parser
