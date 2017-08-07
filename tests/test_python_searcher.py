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

    @staticmethod
    def valid_path(some_file):
        import os
        return ((not some_file.endswith('m') and len(some_file) > 5)
                and not some_file.endswith('-config')
                and os.path.isfile(some_file)
                and not os.path.islink(some_file))

    def test_whereis(self):
        import subprocess
        import os
        import itertools
        import re
        import collections
        python_list = [
            'python',
            'ironpython',
            'anaconda',
            'miniconda',
            'jython',
            'micropython',
            'pypy',
            'pyston',
            'stackless',
        ]

        collected = collections.OrderedDict()
        for python_version in python_list:
            # python_version = 'pypy'
            raw_result = subprocess.check_output(['whereis', python_version])
            raw_result = raw_result.decode()
            found_python_versions = raw_result.replace(python_version+': ', '')

            new_list = [found_path for found_path
                        in found_python_versions.strip().split(' ')
                        if self.valid_path(found_path)]
            if not new_list:
                continue
            for ver in new_list:
                try:
                    raw_result = subprocess.check_output([ver, '-V'], stderr=subprocess.STDOUT)
                    raw_result = raw_result.decode()
                    if not raw_result:
                        continue
                    print(raw_result)
                except subprocess.CalledProcessError:
                    continue

                py_version = str(python_version)
                if ver not in raw_result.lower():
                    py_version = raw_result.split(' ')[0]
                # version = raw_result
                raw_result = raw_result.replace('\n', ' ')[:-1]
                raw_result = re.sub(r'\(.*\) ', '', raw_result)
                try:
                    internal_dict = collected[raw_result]
                    try:
                        internal_dict[os.path.basename(ver)].append(ver)
                    except KeyError:
                        internal_dict[os.path.basename(ver)] = [ver]
                except KeyError:
                    collected[raw_result] = collections.OrderedDict()
                    collected[raw_result][os.path.basename(ver)] = [ver]
        import json
        print(json.dumps(collected, indent=4))
        self.assertEqual('qweqw', '')
