"""Main command line options"""
import sys

SUCCESSCODE = 0
WARNINGCODE = 1
ERRORCODE = 2


def main():
    """Commandline Entrypoint"""
    return ERRORCODE, "USAGE: " + sys.argv[0]
