"""TestModule which tests main function."""
import unittest

import hardest.command_line as commandline
import mock  # type: ignore


class TestUsage(unittest.TestCase):
    """Test usage."""

    def test_command_line_exists(self):
        """Test command_line entry point import/exists."""
        sys_path = 'hardest.command_line.sys'
        print_path = 'argparse.ArgumentParser._print_message'

        version = "hardest 0.0.1\n"

        with mock.patch(sys_path) as patch:
            patch.argv = ['hardest', '-v']
            with mock.patch(print_path) as printpatch:
                with self.assertRaises(SystemExit) as sysexit:
                    commandline.main()
                self.assertEqual(sysexit.exception.code, 0)
                printpatch.assert_called_once_with(version,
                                                   mock.ANY)

    def test_command_line_exists2(self):
        """Test command_line entry point import/exists."""
        with self.assertRaises(SystemExit) as sysexit:
            commandline.main_exit('\nTestHelloMessage', 0)
        self.assertEqual(sysexit.exception.code, 0)
