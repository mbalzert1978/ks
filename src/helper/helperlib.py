import getpass
import io
import string
import sys
from contextlib import redirect_stdout
from pathlib import Path

import black
import peewee as pw
from pwiz import make_introspector, print_models


def extract_header(table: pw.ModelBase) -> list[str]:
    header = list(table.select().dicts()[0].keys())
    return header


def get_model_str(args):
    ispector = make_introspector("sqlite", args[-1])
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print_models(ispector)
    return buffer.getvalue()


def replace_unknown_fields_to_text_fields(model: str):
    return model[:158] + model[159:].replace(r"UnknownField", r"TextField")


def save_model_to_file(model: str):
    with Path(Path.cwd() / "model.py") as file:
        file.touch()
        file.write_text(model)


def get_connect_kwargs(options):
    ops = ("host", "port", "user")
    kwargs = dict((o, getattr(options, o)) for o in ops if getattr(options, o))
    if options.password:
        kwargs["password"] = getpass()
    return kwargs


def err(msg) -> None:
    sys.stderr.write("\033[91m%s\033[0m\n" % msg)
    sys.stderr.flush()


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


def fix_file_extension_csv(filename: str) -> str:
    """
    checks the given filename for the extension .csv
    and appends it if necessary.
    :filename:`str`
    """
    if not filename.endswith(".csv"):
        filename += ".csv"
    return filename


class Validator:
    @staticmethod
    def validate_filepath(s) -> bool:
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return all(c for c in s if c in valid_chars)

    @staticmethod
    def is_model():
        return Path("src/model/model.py").is_file()
