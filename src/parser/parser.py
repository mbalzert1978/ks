import argparse
from pathlib import Path


def get_main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    ap = parser.add_argument
    ap(
        dest="database",
        help="URI of the database you want to access."
        "Example: 'sqlite:///database.db'",
    )
    ap(dest="table", help="Name of the table you want to access.", type=str)
    ap(
        dest="filename",
        help="The filename to use for the output file. Default = 'tablename.csv'",
        default="",
    )
    ap(
        "-d",
        "--delimiter",
        dest="delimiter",
        help="The delimiter to use for the output file. Default = ';'",
        default=";",
    )
    mut = parser.add_mutually_exclusive_group()
    gp = mut.add_argument
    gp(
        "-j",
        "--json",
        dest="json",
        help="Generate a JSON representation of the table.",
        action="store_true",
    )
    gp(
        "-c",
        "--csv",
        dest="csv",
        help="Generate a CSV representation of the table.",
        action="store_true",
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
