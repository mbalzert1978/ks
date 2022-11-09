import sys

from .helperlib import err, format_str, save_model_to_file
from .model.model_creator import Creator
from .model.sqlite_connection import Sq3LiteConnection


def create_model(args) -> str:
    sqlite = Sq3LiteConnection(db=args)
    create = Creator(sqlite)
    model = create.create_model()
    model = format_str(model)
    return model


def main() -> None:
    raw_argv = sys.argv
    *_, db = raw_argv
    if len(raw_argv) < 1:
        err('Missing required parameter "database"')
        sys.exit(1)
    model = create_model(db)
    save_model_to_file(model)
