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

# from functools import reduce  # pylint: disable=redefined-builtin

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
        self.env['PATH'] = self.binpath[:-1] + ':' + current_path

        current_path = self.env.get('PATH', '')
        wrongpath = os.getcwd() + '/not_exist/'  # type: str
        self.env['PATH'] = wrongpath + ':' + current_path
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
        with self.assertRaises(TypeError):  # type: ignore
            pysearch.PythonSearcher(validator='not validator')  # type: ignore

    def test_python_version_str(self):
        # type: () -> None
        """Test version python __str__ method."""
        from hardest.python_version import PythonVersion
        bins = {
            self.binpath + 'python',
            self.binpath + 'python1.2',
        }
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

    def test_get_versions(self):
        # type: () -> None
        """Test get_python_versions search my python bins."""
        import hardest.python_searcher as pysearch
        from hardest.python_version import PythonVersion

        instance = pysearch.PythonSearcher(env=self.env,
                                           validator=self.validator)

        test_versions_paths = {
            self.binpath + 'python',
            self.binpath + 'python1.2',
            self.binpath + 'jython9.1',
            self.binpath + 'anaconda',
            self.binpath + 'raisecode',
        }
        test_versions = {
            PythonVersion('Python test.1.2', {
                self.binpath + 'python',
                self.binpath + 'python1.2',
            }),
            PythonVersion('Jython test.9.1', {
                self.binpath + 'jython9.1',
            }),
            PythonVersion('Anaconda test.3.1', {
                self.binpath + 'anaconda',
            }),
        }
        bad_version = PythonVersion('Unknown', {
            self.binpath + 'raisecode',
        })
        found_vers = set(instance.get_python_versions(test_versions_paths))
        self.assertEqual(test_versions & found_vers, test_versions)
        self.assertIn(bad_version, instance.bad_versions)

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
        from hardest.python_searcher import PythonVersion

        instance = PythonSearcher(env=self.env, validator=self.validator)
        found_versions = set(instance.search())

        test_versions = set((
            PythonVersion('Python test.1.2', set((
                self.binpath + 'python',
                self.binpath + 'python1.2',
            ))),
            PythonVersion('Jython test.9.1', set((
                self.binpath + 'jython9.1',
            ))),
            PythonVersion('Anaconda test.3.1', set((
                self.binpath + 'anaconda',
            ))),
        ))
        self.assertEqual(test_versions & found_versions, test_versions)

    def test_path_files_searcher(self):
        # type: () -> None
        """Test path files."""
        from hardest.python_searcher import PythonSearcher
        instance = PythonSearcher(env=self.env, validator=self.validator)
        data = instance._search_vars_in_path()  # pylint: disable-all
        self.assertIn(self.binpath + 'python', data)
        self.assertIn(self.binpath + 'python1.2', data)
