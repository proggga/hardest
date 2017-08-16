"""Test python_searcher class.

Should search next python implementations:
    python
    anaconda
    ironpython
    jython
    micropython
    miniconda
    pypy
    pyston
    stackless
"""
import os
import unittest

from typing import Dict  # noqa pylint: disable=unused-import
from typing import Set   # noqa pylint: disable=unused-import
from typing import List  # noqa pylint: disable=unused-import

import mock  # type: ignore

from hardest.binary_validator import BinaryValidator


class SimpleTestValidator(BinaryValidator):  # noqa pylint: disable=R0903,W0232
    """Validate is binary file is valid."""

    def __init__(self, path):
        # type: (str) -> None
        """Store path for tests."""
        self.path = path

    def validate(self, data):  # pragma: no cover
        # type: (object) -> bool
        """Validate if in test dir and executable."""
        filename = str(data)
        print('yoho, data', data)
        if not filename.startswith(self.path):
            return False
        return super(SimpleTestValidator, self).validate(filename)


class PythonSearcherTestCase(unittest.TestCase):
    """Test case for it."""

    def setUp(self):
        # type: () -> None
        """Create test env for os methods."""
        self.env = os.environ.copy()  # type: Dict[str, str]
        self.binpath = os.getcwd() + '/tests/bindemo/'  # type: str
        current_path = self.env.get('PATH', '')  # type: str
        self.env['PATH'] = self.binpath + ':' + current_path
        self.evnironpath = ('hardest.python_searcher'
                            '.os.environ')  # type: str
        self.validcheck_path = ('hardest.python_searcher'
                                '.PythonSearcher.get_validator')  # type: str

    def test_get_versions(self):
        # type: () -> None
        """Test get_python_versions search my python bins."""
        import hardest.python_searcher

        instance = hardest.python_searcher.PythonSearcher()

        test_versions = {}  # type: Dict[str, str]
        test_versions = {
            self.binpath + 'python': 'Python test.1.2',
            self.binpath + 'python1.2': 'Python test.1.2',
            self.binpath + 'jython9.1': 'Jython test.9.1',
            self.binpath + 'anaconda': 'Anaconda test.3.1',
        }
        versions = list(test_versions.keys())
        found_vers = []  # type: List[hardest.python_searcher.PythonVersion]
        with mock.patch(self.evnironpath) as envpatch:  # type: ignore
            envpatch.copy.return_value = self.env  # type: ignore
            with mock.patch(self.validcheck_path) as getval:
                getval.return_value = SimpleTestValidator(self.binpath)
                found_vers = instance.get_python_versions(versions)
        should_be_values = test_versions.values()
        for pyver in found_vers:
            if pyver.version in should_be_values:
                for foundbin in pyver.binaries:
                    self.assertIn(foundbin, test_versions)
                    self.assertEqual(pyver.version,
                                     test_versions[foundbin])
                    del test_versions[foundbin]
        empty_dict = {}  # type: Dict[str, str]
        self.assertDictEqual(test_versions, empty_dict)

    def test_valid_path(self):
        # type: () -> None
        """Test vinary get valid files list."""
        from hardest.python_searcher import PythonSearcher
        instance = PythonSearcher()
        files = set()  # type: Set[str]
        with mock.patch(self.evnironpath) as patched:  # type: ignore
            patched.copy.return_value = self.env  # type: ignore
            with mock.patch(self.validcheck_path) as getval:
                getval.return_value = SimpleTestValidator(self.binpath)
                files = instance.get_valid_files('python')
        self.assertIn(self.binpath + 'python', files)
        self.assertIn(self.binpath + 'python1.2', files)

        with mock.patch(self.evnironpath) as patched:  # type: ignore
            with mock.patch(self.validcheck_path) as getval:
                getval.return_value = SimpleTestValidator(self.binpath)
                patched.copy.return_value = self.env  # type: ignore
                files = instance.get_valid_files('jython')
        self.assertIn(self.binpath + 'jython9.1', files)

        with mock.patch(self.evnironpath) as patched:  # type: ignore
            patched.copy.return_value = self.env  # type: ignore
            with mock.patch(self.validcheck_path) as getval:
                getval.return_value = SimpleTestValidator(self.binpath)
                files = instance.get_valid_files('anaconda')
        self.assertIn(self.binpath + 'anaconda', files)

    def test_search(self):
        # type: () -> None
        """Test full search of versions."""
        from hardest.python_searcher import PythonSearcher
        instance = PythonSearcher()
        found_versions = []
        with mock.patch(self.evnironpath) as envpatch:  # type:ignore
            envpatch.copy.return_value = self.env  # type: ignore
            with mock.patch(self.validcheck_path) as getval:
                getval.return_value = SimpleTestValidator(self.binpath)
                found_versions = instance.search()

        test_versions = {}  # type: Dict[str, List[str]]
        test_versions = {
            'Python test.1.2': set((
                self.binpath + 'python',
                self.binpath + 'python1.2',
            )),
            'Jython test.9.1': set([self.binpath + 'jython9.1']),
            'Anaconda test.3.1': set([self.binpath + 'anaconda']),
        }
        for version, bins in test_versions.items():
            found = None
            for pyver in found_versions:
                if pyver.version == version:
                    found = pyver
                    break
            self.assertTrue(found)
            self.assertEqual(found.binaries, bins)
