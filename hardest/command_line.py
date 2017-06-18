"""Main command line options."""
import sys

import argparse

SUCCESSCODE = 0
WARNINGCODE = 1
ERRORCODE = 2


def main():
    """Commandline Entrypoint."""
    parser = argparse.ArgumentParser(add_help=True,
                                     description='Hardest - hard test utils')
    parser.add_argument('--version', '-v', action='version',
                        version=sys.argv[0] + ' 0.0.1')
    parser.add_argument('--hello', dest='hello',
                        action='store_true',
                        help='type hello to get world')
    args = parser.parse_args(args=sys.argv[1:])
    args_dict = vars(args)
    return SUCCESSCODE, 'world!' if args_dict['hello'] else 'home'