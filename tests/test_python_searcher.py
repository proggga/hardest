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
import unittest


class PythonSearcherTestCase(unittest.TestCase):
    """Test case for it."""

    def test_get_versions(self):
        """Test version search properly."""
        from hardest.python_searcher import PythonSearcher
        instance = PythonSearcher()
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
        files = instance.get_valid_files('python')
        for version in files:
            print('', version)
        self.assertTrue(files)

    def test_search(self):
        """Test full search of versions."""
        from hardest.python_searcher import PythonSearcher
        instance = PythonSearcher()
        found_versions = instance.search()
        for version in found_versions:
            print('', version.version)
            for binar in version.binaries:
                print('--> ', binar)
        self.assertTrue(not found_versions)
