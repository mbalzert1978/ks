import argparse
import sys
from pwiz import print_models, make_introspector


def create_parser(args) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "Script to create an model to connect to an SQLite database."
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
        "-m",
        "--modelname",
        help="Name of the model. Default = model.py",
        default="model.py",
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    args = create_parser(sys.argv[1:])
    intro = make_introspector("sqlite", args.database)
    with open(args.modelname, "w") as sys.stdout:
        print_models(intro)
