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

    def test_equality(self):
        # type: () -> None
        """Test equality."""
        valid_file1 = os.getcwd() + '/tests/bindemo/python'
        valid_file2 = os.getcwd() + '/tests/bindemo/python1.2'
        from hardest.binary import Binary
        first = Binary(valid_file1)
        second = Binary(valid_file2)
        self.assertNotEqual(first, second)

        self.assertEqual(first, first)

        same_as_first = Binary(valid_file1)
        self.assertEqual(first, same_as_first)

        self.assertNotEqual(first, 'some_text')

        self.assertNotEqual(first, 10)

    def test_hashes(self):
        # type: () -> None
        """Test hash works equal."""
        valid_file1 = os.getcwd() + '/tests/bindemo/python'
        valid_file2 = os.getcwd() + '/tests/bindemo/python1.2'
        from hardest.binary import Binary
        first = Binary(valid_file1)
        self.assertEqual(hash(first), hash(first))

        second = Binary(valid_file2)
        self.assertNotEqual(hash(first), hash(second))

        first_new = Binary(valid_file1)
        self.assertEqual(hash(first), hash(first_new))

    def test_raise(self):
        # type: () -> None
        """Test true if file is valid."""
        bad_file = os.getcwd() + '/tests/bindemo/raisecode'
        from hardest.binary import Binary
        binar = Binary(bad_file)
        self.assertEqual(binar.version(), 'Unknown')

    def test_str(self):
        # type: () -> None
        """Test str method."""
        bad_file = os.getcwd() + '/tests/bindemo/raisecode'
        from hardest.binary import Binary
        self.assertEqual(str(Binary(bad_file)), bad_file + ' (Unknown)')

        valid_file = os.getcwd() + '/tests/bindemo/python'
        self.assertEqual(str(Binary(valid_file)),
                         valid_file + ' (Python test.1.2)')

    def test_repr(self):
        # type: () -> None
        """Test __repr__ method."""
        bad_file = os.getcwd() + '/tests/bindemo/raisecode'
        from hardest.binary import Binary
        self.assertEqual(repr(Binary(bad_file)),
                         'Binary obj ({}, Unknown)'.format(bad_file))

        valid_file = os.getcwd() + '/tests/bindemo/python'
        self.assertEqual(repr(Binary(valid_file)),
                         'Binary obj ({}, Python test.1.2)'.format(valid_file))
