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
    ap(
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
        help="The filename to use for the output.csv file.",
        default=False,
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
