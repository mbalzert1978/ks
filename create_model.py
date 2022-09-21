import argparse
import io
import sys
from contextlib import redirect_stdout

import black
from pwiz import make_introspector, print_models


def create_parser(args) -> argparse.Namespace:
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


def create_model(args):
    model = get_model_str(args)
    model = fix_unknown_fields(model)
    model = format_str(model)
    return model


def format_str(model: str):
    return black.format_str(
        model,
        mode=black.Mode(
            target_versions={black.TargetVersion.PY36},
            line_length=79,
            string_normalization=False,
            is_pyi=False,
        ),
    )


def get_model_str(args):
    intro_spector = make_introspector("sqlite", args.database)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print_models(intro_spector)
    return buffer.getvalue()


def fix_unknown_fields(model: str):
    return model[:158] + model[159:].replace(r"UnknownField", r"TextField")


def save_model(args, model: str):
    with open(args.modelname, "w") as file:
        file.writelines(model)


if __name__ == "__main__":
    args = create_parser(sys.argv[1:])
    model = create_model(args)
    save_model(args, model)
