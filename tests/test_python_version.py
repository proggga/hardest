"""Test PythonVersion."""
import os
import unittest

from typing import Set  # noqa pylint: disable=unused-import
from typing import Dict  # noqa pylint: disable=unused-import


class PythonVersionTestCase(unittest.TestCase):
    """Test case for it."""

    def setUp(self):
        # type: () -> None
        """Create test env for os methods."""
        self.env = os.environ.copy()  # type: Dict[str, str]
        self.binpath = os.getcwd() + '/tests/bindemo/'  # type: str

    def test_python_version_str(self):
        # type: () -> None
        """Test version python __str__ method."""
        from hardest.python_version import PythonVersion
        bins = {
            self.binpath + 'python',
            self.binpath + 'python1.2',
        }  # type: Set[str]
        pyver = PythonVersion('Python test.1.2', bins)
        shouldbe = "v: Python test.1.2 ({})".format(str(bins))
        self.assertEqual(str(pyver), shouldbe)

    def test_python_version_repr(self):
        # type: () -> None
        """Test version python __repr__ method."""
        from hardest.python_version import PythonVersion
        bins = {
            self.binpath + 'python',
            self.binpath + 'python1.2',
        }
        pyver = PythonVersion('Python test.1.2', bins)
        shouldbe = ("PythonVersion object: Python test.1.2 ({})"
                    .format(str(bins)))
        self.assertEqual(repr(pyver), shouldbe)

    def test_python_version_eq(self):
        # type: () -> None
        """Test version python __repr__ method."""
        from hardest.python_version import PythonVersion
        bins = {
            self.binpath + 'python',
            self.binpath + 'python1.2',
        }
        pyver1 = PythonVersion('Python test.1.2', bins)
        self.assertEqual(pyver1, pyver1)

        pyver2 = PythonVersion('Python test.1.2', bins)
        self.assertEqual(pyver1, pyver2)

        pyver3 = PythonVersion('Python test.1.2', set([]))
        self.assertNotEqual(pyver1, pyver3)

        pyver4 = PythonVersion('Python test.1.3', bins)
        self.assertNotEqual(pyver1, pyver4)

        self.assertNotEqual(pyver1, 'some_text')
