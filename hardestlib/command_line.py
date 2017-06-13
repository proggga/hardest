"""Main command line options"""

SUCCESSCODE = 0
WARNINGCODE = 1
ERRORCODE = 2


def main():
    """Commandline Entrypoint"""
    print("I am here!", "do this please")
    return ERRORCODE, "USAGE"
