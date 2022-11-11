import sys
from src.helper.helperlib import Validator, err
from .parser.parser import get_main_parser
from .extractor.extractor import Extractor
from .facade.csv import CSV
import model


def main() -> None:
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
    get_table(args, model)


def get_table(args, model) -> None:
    sql = Extractor(model, args.database)
    result = sql.select_table(args.table)
    if args.filename:
        csv = CSV(result)
        csv.write(args.filename, args.delimiter)
    else:
        print(result)
