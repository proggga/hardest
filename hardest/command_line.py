"""Main command line options."""
import sys

from typing import Dict  # noqa pylint: disable=unused-import
from typing import Any  # noqa pylint: disable=unused-import

import argparse

SUCCESSCODE = 0
ERRORCODE = 2


def main():
    # type: () -> None
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
    # help(args)
    # args_dict = vars(args)  # type: Dict[str, Any]
    str_dict = {}  # type: Dict[str, str]
    str_dict = {str(key): str(value)
                for key, value in vars(args).items()}
    # package_name = 'hardest'
    # resource_path = '/'.join(('templates', 'tox.ini.jn2'))
    #
    message_text = 'home'
    if str_dict['--hello']:
        message_text = 'world!'
    success(message_text)


def success(message):
    # type: (str) -> None
    """Exit with success exit code."""
    main_exit(message, SUCCESSCODE)


def failure(message):
    # type: (str) -> None
    """Exit with failure exit code."""
    main_exit(message, ERRORCODE)


def main_exit(message, exitcode):
    # type: (str, int) -> None
    """Exit with message and code."""
    print("", message)
    sys.exit(exitcode)
