"""TestModule which tests hello"""
import unittest

import hardest.command_line as commandline
import mock


class Testhelloworld(unittest.TestCase):
    """Tests hello command"""

    def test_world_command(self):
        """Test"""

        sys_path = 'hardest.command_line.sys'
        print_path = 'argparse.ArgumentParser._print_message'
        with mock.patch(sys_path) as patch:
            patch.argv = ['hardest', '--hello']
            with mock.patch(print_path):
                code, message = commandline.main()
                self.assertEqual(message, 'world!')
                self.assertEqual(code, 0)

    def test_home_command(self):
        """Test"""

        sys_path = 'hardest.command_line.sys'
        print_path = 'argparse.ArgumentParser._print_message'
        with mock.patch(sys_path) as patch:
            patch.argv = ['hardest']
            with mock.patch(print_path):
                code, message = commandline.main()
                self.assertEqual(message, 'home')
                self.assertEqual(code, 0)
