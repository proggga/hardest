"""Test binary validator."""
import os

import unittest


class BinaryValidtorTestCase(unittest.TestCase):
    """Test case for validator."""

    def setUp(self):
        """Test setup."""
        from hardest.binary_validator import BinaryValidator
        self.instance = BinaryValidator()

    def test_empty_path_fails(self):
        # type: () -> None
        """Test false if file empty."""
        self.assertFalse(self.instance.validate(""))

    def test_config_suffix_fails(self):
        # type: () -> None
        """Test false if file ends with '-config'."""
        file_with_config = os.getcwd() + '/tests/bindemo/python-config'
        self.assertFalse(self.instance.validate(file_with_config))

    def test_without_exec_right_fails(self):
        # type: () -> None
        """Test false if file non executable."""
        nonexec = os.getcwd() + '/tests/bindemo/non_exec_file'
        self.assertFalse(self.instance.validate(nonexec))

    def test_file_is_link_fails(self):
        # type: () -> None
        """Test false if file is link."""
        link_file = os.getcwd() + '/tests/bindemo/linkpython'
        self.assertFalse(self.instance.validate(link_file))

    def test_valid_python_file(self):
        # type: () -> None
        """Test true if file is valid."""
        valid_file = os.getcwd() + '/tests/bindemo/python'
        self.assertTrue(self.instance.validate(valid_file))
