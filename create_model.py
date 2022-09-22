import io
import sys
from contextlib import redirect_stdout
from getpass import getpass
from optparse import OptionParser

import black
from pwiz import make_introspector, print_models


def err(msg):
    sys.stderr.write("\033[91m%s\033[0m\n" % msg)
    sys.stderr.flush()


def get_option_parser():
    parser = OptionParser(usage="usage: %prog [options] database_name")
    ao = parser.add_option
    ao("-H", "--host", dest="host")
    ao("-p", "--port", dest="port", type="int")
    ao("-u", "--user", dest="user")
    ao("-P", "--password", dest="password", action="store_true")
    return parser


def get_connect_kwargs(options):
    ops = ("host", "port", "user")
    kwargs = dict((o, getattr(options, o)) for o in ops if getattr(options, o))
    if options.password:
        kwargs["password"] = getpass()
    return kwargs


def create_model(args):
    model = get_model_str(args)
    model = replace_unknown_fields_to_text_fields(model)
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
    ispector = make_introspector("sqlite", args[-1])
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print_models(ispector)
    return buffer.getvalue()


def replace_unknown_fields_to_text_fields(model: str):
    return model[:158] + model[159:].replace(r"UnknownField", r"TextField")


def save_model_to_file(model: str):
    with open("model.py", "w") as file:
        file.writelines(model)


def main(args):
    model = create_model(args)
    save_model_to_file(model)


if __name__ == "__main__":
    raw_argv = sys.argv
    parser = get_option_parser()
    options, args = parser.parse_args()
    if len(args) < 1:
        err('Missing required parameter "database"')
        parser.print_help()
        sys.exit(1)
    connect = get_connect_kwargs(options)
    database = args[-1]
    main(args)
