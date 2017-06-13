"""Main command line options"""
import sys
import argparse

SUCCESSCODE = 0
WARNINGCODE = 1
ERRORCODE = 2


def main():
    """Commandline Entrypoint"""
    parser = argparse.ArgumentParser(add_help=True,
                                     description='Hardest - hard test utils')
    parser.add_argument('--version', '-v', action='version',
                        version=sys.argv[0] + ' 0.0.1')
    args = parser.parse_args(sys.argv[1:])
    return SUCCESSCODE, str(args)
