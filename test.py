import sys

from src.helper.helperlib import Validator, err
from src.parser.option_parser import get_main_parser


if __name__ == "__main__":
    raw_argv = sys.argv
    if not Validator.is_model():
        err("Missing required file 'model.py'.")
        print("Use create_model.py to create a model.")
        sys.exit(1)

    parser = get_main_parser()
    args = parser.parse_args()
    print()
