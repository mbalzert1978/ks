import sys

from src.helper.helperlib import Validator, err
from src.main import main
from src.parser.parser import get_main_parser


if __name__ == "__main__":
    if not Validator.is_model():
        err("Missing required file 'model.py'.")
        print("Use create_model.py to create a model.")
        sys.exit(1)
    import model

    parser = get_main_parser()
    args = parser.parse_args()
    if len(args.delimiter) > 1:
        err('"delimiter" must be one character.')
        parser.print_help()
        sys.exit(1)
    if args.filename:
        if not Validator.validate_filepath(args.filename):
            err('"filename" must be a valid file/path.')
            parser.print_help()
            sys.exit(1)
    main(args, model)
# sqlite_file_name = "database.db"
# sqlite_uri = f"sqlite:///{sqlite_file_name}"
