import sys

from src.helper.helperlib import (
    err,
    format_str,
    get_model_str,
    replace_unknown_fields_to_text_fields,
    save_model_to_file,
)
from src.parser.option_parser import get_option_parser


def create_model(args):
    model = get_model_str(args)
    model = replace_unknown_fields_to_text_fields(model)
    model = format_str(model)
    return model


def main():
    parser = get_option_parser(False)
    _, args = parser.parse_args()
    if len(args) < 1:
        err('Missing required parameter "database"')
        parser.print_help()
        sys.exit(1)
    model = create_model(args)
    save_model_to_file(model)
