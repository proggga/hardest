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

from hardest.python_version import PythonVersion


class PythonSearcherTestCase(unittest.TestCase):
    """Test case for it."""

    def setUp(self):
        # type: () -> None
        """Create test env for os methods."""
        # Preparing env with paths
        self.env_original = os.environ.copy()  # type: Dict[str, str]
        self.testpath_no_slash = os.getcwd() + '/tests/bindemo'  # type: str
        self.testpath = self.testpath_no_slash + '/'  # type: str
        self.external_path = os.getcwd() + '/tests/bindemo/another/'  # type: str
        self.wrongpath = os.getcwd() + '/not_exist'  # type: str
        self.env = self._get_test_env()  # type: Dict[str, str]

        self.test_list = {}  # type: Dict[str, List[PythonVersion]]
        self.test_list = {
            'jython9.1': [
                PythonVersion('Jython test.9.1', {
                    self.testpath + 'jython9.1',
                }),
            ],
            'anaconda': [
                PythonVersion('Anaconda test.3.1', {
                    self.testpath + 'anaconda',
                }),
            ],
            'UNKNOWN': [
                PythonVersion('Unknown', {
                    self.testpath + 'raisecode',
                })
            ],
        }

    def _get_test_env(self, reverse=False):
        # type: (bool) -> Dict[str, str]
        """Add path to PATH var."""
        path_list = []  # type: List[str]
        path_list = [
            self.testpath_no_slash,
            self.external_path[:-1],
            self.wrongpath,
        ]
        if reverse:
            path_list = list(reversed(path_list))

        env = dict(self.env_original)  # type: Dict[str, str]
        env_path = env.get('PATH', '')  # type: str
        if env_path:
            env['PATH'] = ':'.join(path_list) + ':' + env_path
        return env

    @unittest.skip('integration test, not works.')
    def test_get_versions(self):
        # type: () -> None
        """Test get_python_versions search my python bins."""
        import hardest.python_searcher as pysearch

        instance = pysearch.PythonSearcher(env=self.env)
        test_list = {}  # type: Dict[str, List[PythonVersion]]
        test_list = dict(self.test_list)
        test_list['python'] = [
            PythonVersion('Python test.1.2', {
                self.testpath + 'python',
                self.testpath + 'python1.2',
            }),
            PythonVersion('Python test.0.2', {
                self.external_path + 'python',
            })
        ]
        test_keys = set(test_list.keys())

        found_vers = instance.search()  # Dict[str, PythonVersion]
        found_keys = set(found_vers.keys())  # type: ignore

        self.assertEqual(test_keys & found_keys, test_keys)
        for key, values in test_list.items():  # type: str, List[PythonVersion]
            test_versions = set(values)
            found_versions = set(found_vers[key])
            self.assertEqual(test_versions & found_versions, test_versions)


    def test_get_files_from_env(self):
        # type: () -> None
        """Test get_python_versions search my python bins."""
        import hardest.python_searcher as pysearch

        instance = pysearch.PythonSearcher(env=self.env)
        self.assertTrue(hasattr(instance, 'get_files_from_env'))

        files = instance.get_files_from_env()
        self.assertIn(self.testpath + 'python', files)
        self.assertIn(self.testpath + 'python1.2', files)
        self.assertIn(self.external_path + 'python', files)
