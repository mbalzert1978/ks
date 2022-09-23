import optparse
import sys

from src.helper.helperlib import Validator, err, get_connect_kwargs
from src.main import main
from src.parser.option_parser import get_option_parser

options: optparse.Values
args: list[str]
nl: str


if __name__ == "__main__":
    raw_argv = sys.argv
    if not Validator.is_model():
        err("Missing required file 'model.py'.")
        print("Use create_model.py to create a model.")
        sys.exit(1)
    import src.model.model as model

    parser = get_option_parser(True)
    options, args = parser.parse_args()
    if len(args) < 1:
        err('Missing required parameter "database".')
        parser.print_help()
        sys.exit(1)
    if len(options.delimiter) > 1:
        err('"delimiter" must be a 1-character string.')
        parser.print_help()
        sys.exit(1)
    if options.filename:
        if not Validator.validate_filepath(options.filename):
            err('"filename" must be a valid file/path.')
            parser.print_help()
            sys.exit(1)
    main(options, model)
