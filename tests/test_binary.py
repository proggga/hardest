"""Test binary."""
import os

import unittest


class BinaryTestCase(unittest.TestCase):
    """Test case for Binary class."""

    def test_without_exec_right_fails(self):
        # type: () -> None
        """Test false if file non executable."""
        nonexec = os.getcwd() + '/tests/bindemo/non_exec_file'
        from hardest.binary import Binary
        binar = Binary(nonexec)
        self.assertEqual(binar.version(), 'Error')

    def test_valid_python_file(self):
        # type: () -> None
        """Test true if file is valid."""
        valid_file = os.getcwd() + '/tests/bindemo/python'
        from hardest.binary import Binary
        binar = Binary(valid_file)
        self.assertEqual(binar.version(), 'Python test.1.2')

    def test_unicode(self):
        # type: () -> None
        """Test true if file is valid."""
        valid_file = os.getcwd() + '/tests/bindemo/printunicode'
        from hardest.binary import Binary
        binar = Binary(valid_file)
        self.assertEqual(binar.version(), 'Unknown')

    def test_raise(self):
        # type: () -> None
        """Test true if file is valid."""
        valid_file = os.getcwd() + '/tests/bindemo/raisecode'
        from hardest.binary import Binary
        binar = Binary(valid_file)
        self.assertEqual(binar.version(), 'Unknown')
