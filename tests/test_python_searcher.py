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


class PythonSearcherTestCase(unittest.TestCase):
    """Test case for it."""

    def setUp(self):
        # type: () -> None
        """Create test env for os methods."""
        # Preparing env with paths
        self._env_original = os.environ.copy()  # type: Dict[str, str]
        cwd = os.getcwd()
        self.testpath_no_slash = cwd + '/tests/bindemo'  # type: str
        self.testpath = self.testpath_no_slash + '/'     # type: str
        self.external_path = self.testpath + 'another/'   # type: str
        self.wrongpath = cwd + '/not_exist'              # type: str

        self.test_list = {}  # type: Dict[str, List[PythonVersion]]
        self.test_list = {
            'python': [],
            'python1.2': [],
            'jython9.1': [],
            'anaconda': [],
        }

    def _get_prepared_env(self, reverse=False):
        # type: (bool) -> Dict[str, str]
        """Add path to PATH var."""
        path_list = []  # type: List[str]
        path_list = [
            self.testpath,
            self.external_path,
            self.wrongpath,
        ]

        if reverse:
            path_list = list(reversed(path_list))

        path_list.append('/usr/bin/')

        env = dict(self._env_original)  # type: Dict[str, str]
        # env_path = env.get('PATH', '')  # type: str

        env['PATH'] = ':'.join(path_list)

        return env

    def test_search_return_default_keys(self):
        # type: () -> None
        """Test get_python_versions search my python bins."""
        import hardest.python_searcher as pysearch

        instance = pysearch.PythonSearcher(env=self._get_prepared_env())
        expected = dict(self.test_list)  # type: Dict[str, List[PythonVersion]]
        expected_keys = set(expected.keys())

        actual_data = instance.search()  # Dict[str, Any]
        actual_keys = set(actual_data.keys())  # type: ignore

        print("actual_data", actual_data)
        self.assertEqual(expected_keys & actual_keys, expected_keys)

    def test_search_get_valid_default_from_path(self):
        # type: () -> None
        """Test get_python_versions search my python bins in valid order."""
        import hardest.python_searcher as pysearch

        instance = pysearch.PythonSearcher(env=self._get_prepared_env())

        binaries = instance.search()  # Dict[str, Any]

        default_binary = 0
        self.assertEqual(binaries['python'][default_binary].path,
                          self.testpath + 'python')
        self.assertEqual(binaries['python1.2'][default_binary].path,
                          self.testpath + 'python1.2')

    def test_search_get_valid_default_reversed(self):
        # type: () -> None
        """Test get_python_versions search my python bins in valid order."""
        import hardest.python_searcher as pysearch

        reversed_env = self._get_prepared_env(reverse=True)
        instance = pysearch.PythonSearcher(env=reversed_env)

        actual_data = instance.search()  # Dict[str, Any]

        default_binary = 0
        self.assertEqual(actual_data['python'][default_binary].path,
                          self.external_path + 'python')
        self.assertEqual(actual_data['python1.2'][default_binary].path,
                          self.testpath + 'python1.2')
