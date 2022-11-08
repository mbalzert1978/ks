import getpass
import string
import sys
from pathlib import Path

import black


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
            target_versions={black.TargetVersion.PY310},
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


def create_file(file: Path) -> None:
    """
    :file:`pathlib.Path`
    creates the given file if it does not already exist
    """
    if not file.exists():
        file.touch()


class Validator:
    @staticmethod
    def validate_filepath(s) -> bool:
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return all(c for c in s if c in valid_chars)

    @staticmethod
    def is_model():
        model_file = Path(Path.cwd() / "model.py")
        return model_file.exists()
