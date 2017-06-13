"""TestModule which tests main function"""
import re
import unittest

import hardestlib.command_line as commandline


class TestMainCommandline(unittest.TestCase):
    """Tests files args"""

    def test_command_line_exists(self):
        """Test command_line entry point import/exists"""
        self.assertTrue(hasattr(commandline, 'main'))
        exit_code, message = commandline.main()
        self.assertEqual(exit_code, 2)
        result = re.search('USAGE', message)
        self.assertTrue(result)
