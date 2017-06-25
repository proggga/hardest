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
    parser.add_argument('--hello', dest='--hello',
                        action='store_true',
                        help='type hello to get world')
    parser.add_argument('--init', dest='--init',
                        action='store_true',
                        help='init configs in new project')

    args = parser.parse_args(args=sys.argv[1:])
    args_dict = vars(args)
    main_exit('world!' if args_dict['--hello'] else 'home', SUCCESSCODE)


def main_exit(message, exitcode):
    """Exit with message and code."""
    print("", message)
    sys.exit(exitcode)
