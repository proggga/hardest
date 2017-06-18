"""TestModule which tests main function."""
import os
import unittest

import hardest.command_line as commandline
import mock


class TestHelpCommandLine(unittest.TestCase):
    """Tests help command."""

    def test_command(self):
        """Hello command."""
        os.system('hardest')
        self.assertTrue(2 == 2)

    def test_help_command(self):
        """Test command_line entry point import/exists."""
        usage = ("usage: pytest.py [-h] [--version] [--hello]\n\n"
                 "Hardest - hard test utils\n"
                 "\noptional arguments:\n"
                 "  -h, --help   "
                 "  show this help message and exit\n"
                 "  --version, -v"
                 "  show program's version number and exit\n"
                 "  --hello      "
                 "  type hello to get world\n")
        sys_path = 'hardest.command_line.sys'
        print_path = 'argparse.ArgumentParser._print_message'
        with mock.patch(sys_path) as patch:
            patch.argv = ['hardest', '-h']
            with mock.patch(print_path) as printpatch:
                with self.assertRaises(SystemExit) as sysexit:
                    commandline.main()
                self.assertEqual(sysexit.exception.code, 0)
                printpatch.assert_called_once_with(usage,
                                                   mock.ANY)
