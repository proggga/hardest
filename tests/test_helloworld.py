"""TestModule which tests hello."""
import unittest

import re
from subprocess import PIPE
from subprocess import Popen


class Testhelloworld(unittest.TestCase):
    """Tests hello command."""

    def test_world_command(self):
        """Test hello."""
        process = Popen(['hardest', '--hello'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(str(stdout), '')
        self.assertTrue(re.search(r'world!', str(stdout)))
        self.assertTrue(re.search(r'Progga', str(stdout)))
        self.assertEqual(stderr, b'')
