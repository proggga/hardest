"""TestModule which tests main function"""
import unittest

import hardestlib.command_line as commandline
import mock


class TestUsage(unittest.TestCase):
    """Test usage"""

    def test_command_line_exists(self):
        """Test command_line entry point import/exists"""
        self.assertTrue(hasattr(commandline, 'main'))
        with mock.patch('hardestlib.command_line.sys') as patch:
            with mock.patch('argparse.ArgumentParser.exit') as exitspatch:
                patch.argv = ['hardest', '-v']
                commandline.main()
                args = {'message': 'hardest 0.0.1\n'}
                exitspatch.assert_called_once_with(**args)
