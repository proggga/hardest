"""TestModule which tests main function"""
import unittest

import hardestlib.command_line as commandline
import mock


class TestMainCommandline(unittest.TestCase):
    """Tests files args"""

    def test_command_line_exists(self):
        """Test command_line entry point import/exists"""
        self.assertTrue(hasattr(commandline, 'main'))
        with mock.patch('hardestlib.command_line.sys') as patch:
            patch.argv = ['hardest']
            exit_code, message = commandline.main()
        self.assertEqual(exit_code, 2)
        self.assertEqual('USAGE: hardest', message)
