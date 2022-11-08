import sys

from src.helper.helperlib import err, format_str, save_model_to_file

from .model.create_model import get_model_str


def create_model(args) -> str:
    model = get_model_str(args)
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
