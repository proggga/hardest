"""TestModule which tests hello."""
import unittest

from subprocess import Popen
from subprocess import PIPE
import re


class Testhelloworld(unittest.TestCase):
    """Tests hello command."""

    def test_world_command(self):
        """Test hello."""
        process = Popen(['hardest', '--hello'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        self.assertTrue(re.search(r'world!', str(stdout)))
        self.assertEqual(stderr, b'')
