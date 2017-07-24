"""TestModule which tests main function."""
import unittest

import hardest.command_line as commandline
import mock


class TestHelloAgain(unittest.TestCase):
    """Test usage."""

    def test_command_line_exists(self):  # pylint: disable=no-self-use
        """Test command_line entry point import/exists."""
        sys_path = 'hardest.command_line.sys'
        exit_path = 'hardest.command_line.main_exit'

        with mock.patch(sys_path) as patch:
            patch.argv = ['hardest', '--hello']
            with mock.patch(exit_path) as exitpatch:
                commandline.main()
                exitpatch.assert_called_once_with('world!', 0)
