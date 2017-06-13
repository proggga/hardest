"""TestModule which tests module structure"""
import unittest


class TestFilesStructure(unittest.TestCase):
    """Tests files exists and imports"""

    def test_command_line_entrypoint(self):
        """Test command_line entry point import/exists"""
        try:
            import hardestlib.command_line
            self.assertTrue(hardestlib.command_line)
        except ImportError:  # pragma: no cover
            message = 'command_line should imports, but fail'
            self.fail(message)
