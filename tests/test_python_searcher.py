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

import mock


class PythonSearcherTestCase(unittest.TestCase):
    """Test case for it."""

    def test_get_versions(self):
        """Test version search properly."""
        from hardest.python_searcher import PythonSearcher
        instance = PythonSearcher()
        # my_env["PYTHONPATH"] = os.getcwd()+'/tests/bindemo/'
        # my_env["PATH"] = os.getcwd()+'/tests/bindemo/'+ ':' + my_env["PATH"]
        paths = [
            '/usr/bin/python',
            '/usr/bin/python2',
            '/usr/bin/python3',
        ]
        versions = instance.get_python_versions(paths)
        for version in versions:
            print(version.version, version.binaries)
        self.assertTrue(versions)

    def test_valid_path(self):
        """Test vinary get valid files list."""
        from hardest.python_searcher import PythonSearcher
        instance = PythonSearcher()
        edited_env = os.environ.copy()
        edited_env['PATH'] = (os.getcwd() +
                              '/tests/bindemo/:' +
                              edited_env['PATH'])
        files = []
        with mock.patch('hardest.python_searcher.os') as patched:
            patched.environ.copy.return_value = edited_env
            files = instance.get_valid_files('python')
        print(files)
        for version in files:
            print('', version)
        self.assertTrue(not files)

    def test_search(self):
        """Test full search of versions."""
        from hardest.python_searcher import PythonSearcher
        instance = PythonSearcher()
        found_versions = instance.search()
        for version in found_versions:
            print('', version.version)
            for binar in version.binaries:
                print('--> ', binar)
        self.assertTrue(found_versions)
