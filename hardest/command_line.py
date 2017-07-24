"""Main command line options."""
import sys

import argparse
import pkg_resources

from jinja2 import Template


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
    package_name = 'hardest'

    # Do not use os.path.join()
    resource_path = '/'.join(('templates', 'tox.ini.jn2'))

    template_bytes = pkg_resources.resource_string(package_name, resource_path)
    template_content = str(template_bytes)
    template = Template(template_content)
    # template.filename(filename)
    print(str(template.render(username='Progga')), '')

    main_exit('world!' if args_dict['--hello'] else 'home', SUCCESSCODE)


def main_exit(message, exitcode):
    """Exit with message and code."""
    print("", message)
    sys.exit(exitcode)
