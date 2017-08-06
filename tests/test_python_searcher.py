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

    def test_popen(self):
        """Test."""
        import subprocess
        import os
        my_env = os.environ
        my_env["PYTHONUNBUFFERED"] = "True"
        import pty
        master_fd, slave_fd = pty.openpty()

        proc = subprocess.Popen(['python'],
                                # preexec_fn=os.setsid,
                                stdin=slave_fd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                # executable='/usr/bin/python',
                                # env=my_env,
                                # timeout=True,
                                # universal_newlines=True,
                                # shell=True)
                                shell=False)
        pin = os.fdopen(master_fd, 'w')
        pin.write('exit(42)\n')
        # print(proc.stdout.read())
        # print(proc.stdout.read())
        # print(proc.stdout.read())
        # help(proc)
        import time
        # print(proc.stdout.readline())
        # time.sleep(1)
        # print(proc.stderr.read())
        # slave_fd.write('exit(1)')
        stdout, stderr = proc.communicate()
        print(proc.pid, proc.returncode)
        # time.sleep(10)
        print(stdout, stderr)
        print(stderr)



    @unittest.skip('skipped this case')
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
