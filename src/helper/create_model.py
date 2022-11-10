import sys

from src.parser.option_parser import get_create_model_parser

from .helperlib import err, format_str, save_model_to_file
from .model.model_creator import Creator
from .model.sqlite_connection import Sq3LiteConnection


def create_model(args) -> str:
    sqlite = Sq3LiteConnection(db=args.database)
    create = Creator(sqlite)
    model = create.create_model()
    model = format_str(model)
    return model


def main() -> None:
    parser = get_create_model_parser()
    args = parser.parse_args()
    model = create_model(args)
    save_model_to_file(model)
