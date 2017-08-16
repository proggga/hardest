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

from functools import reduce  # pylint: disable=redefined-builtin

from typing import Dict  # noqa pylint: disable=unused-import
from typing import Set   # noqa pylint: disable=unused-import
from typing import List  # noqa pylint: disable=unused-import

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
        self.validator = SimpleTestValidator(self.binpath)

    def test_construtor_without_args(self):
        # type: () -> None
        """Test constuctor without params."""
        import hardest.python_searcher as pysearch
        instance = pysearch.PythonSearcher()
        some_env = os.environ.copy()
        self.assertEqual(instance.env, some_env)

    def test_constr_bad_validator(self):
        # type: () -> None
        """Test constuctor with bad validator."""
        import hardest.python_searcher as pysearch
        with self.assertRaises(TypeError):
            pysearch.PythonSearcher(validator='Some string, not validator.')

    def test_get_versions(self):
        # type: () -> None
        """Test get_python_versions search my python bins."""
        import hardest.python_searcher as pysearch

        instance = pysearch.PythonSearcher(env=self.env,
                                           validator=self.validator)

        test_versions = {}  # type: Dict[str, str]
        test_versions = {
            self.binpath + 'python': 'Python test.1.2',
            self.binpath + 'python1.2': 'Python test.1.2',
            self.binpath + 'jython9.1': 'Jython test.9.1',
            self.binpath + 'anaconda': 'Anaconda test.3.1',
        }
        bad_version = self.binpath + 'raisecode'
        versions = list(test_versions.keys())
        versions.append(bad_version)
        found_vers = []  # type: List[pysearch.PythonVersion]
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
        self.assertTrue(len(bad_version) >= 1)
        bad_bins = [ver.binaries for ver in instance.bad_versions]
        bad_bin_paths = reduce(lambda x, y: x | y, bad_bins)
        self.assertIn(bad_version, bad_bin_paths)

    def test_valid_path(self):
        # type: () -> None
        """Test vinary get valid files list."""
        from hardest.python_searcher import PythonSearcher
        instance = PythonSearcher(env=self.env, validator=self.validator)
        files = set()  # type: Set[str]
        files = instance.get_valid_files('python')
        self.assertIn(self.binpath + 'python', files)
        self.assertIn(self.binpath + 'python1.2', files)

        files = instance.get_valid_files('jython')
        self.assertIn(self.binpath + 'jython9.1', files)

        files = instance.get_valid_files('anaconda')
        self.assertIn(self.binpath + 'anaconda', files)

    def test_search(self):
        # type: () -> None
        """Test full search of versions."""
        from hardest.python_searcher import PythonSearcher
        instance = PythonSearcher(env=self.env, validator=self.validator)
        found_versions = []
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
