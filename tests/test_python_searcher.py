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

    def test_whereis(self):
        import subprocess
        import os
        import itertools
        import collections
        python_list = [
            'python',
            'ironpython',
            'anaconda',
            'jython',
            'micropython',
            'miniconda',
            'pypy',
            'pyston',
            'stackless',
        ]
        def valid_path(some_file):
            return (not some_file.endswith('m')
                    and not some_file.endswith('-config')
                    and os.path.isfile(some_file)
                    and not os.path.islink(some_file))
        collected = collections.OrderedDict()
        for python_version in python_list:
            # python_version = 'pypy'
            raw_result = subprocess.check_output(['whereis', python_version])
            raw_result = raw_result.decode()
            found_python_versions = raw_result.replace(python_version+': ', '')

            new_list = [found_path for found_path
                        in found_python_versions.strip().split(' ')
                        if valid_path(found_path)]
            if not new_list:
                continue
            for ver in new_list:
                try:
                    raw_result = subprocess.check_output([ver, '-c', '"import os; print(os.__file__)"'], stderr=subprocess.STDOUT)
                    raw_result = raw_result.decode()
                    print(raw_result)
                except subprocess.CalledProcessError:
                    continue
                py_version = python_version
                if raw_result:
                    if ver not in raw_result.lower():
                        py_version = raw_result.split(' ')[0]
                    version = ' '.join(raw_result.splitlines()[0].split(' ')[0:2])
                    try:
                        internal_dict = collected[py_version]
                        try:
                            internal_dict[version].append(ver)
                        except KeyError:
                            internal_dict[version] = [ver]
                    except KeyError:
                        collected[py_version] = collections.OrderedDict()
                        collected[py_version][version] = [ver]
        import json
        print(json.dumps(collected, indent=4))
        self.assertEqual('qweqw', '')
