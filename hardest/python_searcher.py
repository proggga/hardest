"""Module represent PythonSearcher search python binary.

This class helps find available python binary
versions for executing and returns data with version and
binaries.
"""
import os
import sys

from itertools import groupby
from operator import methodcaller

# For Mypy typing
from typing import List      # noqa pylint: disable=unused-import
from typing import Union     # noqa pylint: disable=unused-import
from typing import Dict      # noqa pylint: disable=unused-import
from typing import Tuple     # noqa pylint: disable=unused-import
from typing import Set       # noqa pylint: disable=unused-import

from subprocess import check_output

from hardest.binary import Binary  # noqa pylint: disable=unused-import


class PythonSearcher(object):
    """Seach Python version for you."""

    python_search_list = (
        'python',
        'ironpython',
        'conda',
        'anaconda',
        'miniconda',
        'jython',
        'micropython',
        'pypy',
        'pyston',
        'stackless',
    )  # type: Tuple[str, ...]

    def __init__(self):
        # type: () -> None
        """Searcher constructor."""
        self.found_versions = []  # type: List[PythonVersion]
        self.bad_versions = []  # type: List[PythonVersion]

    def search(self):
        # type: () -> List[PythonVersion]
        """Search python versino and return list of versions."""
        valid_files_list = set()  # type: Set[str]
        for version_to_search in self.python_search_list:  # type: str
            files = self.get_valid_files(version_to_search)
            if not files:
                continue
            valid_files_list.update(set(files))
        print(valid_files_list)
        self.get_python_versions(valid_files_list)

        return self.found_versions

    def get_valid_files(self, version_to_search):
        # type: (str) -> Set[str]
        """Get binaries path for python versions."""
        command = ['/usr/bin/whereis', version_to_search]  # type: List[str]
        environment = os.environ.copy()
        raw_output = check_output(command, env=environment)  # type: bytes
        decoded_output = str(raw_output.decode())  # type: str
        front_unattended_str = '{}:'.format(version_to_search)
        cropped_output = decoded_output.replace(front_unattended_str, '')
        output = cropped_output.strip()
        if not output:
            return []
        files_list = output.split(' ')
        files_set = set(files_list)
        files_set.add(sys.executable)
        return set(filepath for filepath in files_set
                   if self._valid_path(filepath))

    @staticmethod
    def _valid_path(some_file):
        # type: (str) -> bool
        return (bool(some_file) and
                not some_file.endswith('-config') and
                os.path.isfile(some_file) and
                not os.path.islink(some_file) and
                os.access(some_file, os.X_OK))

    def get_python_versions(self, versions):
        # type: (List[str]) -> List[PythonVersion]
        """Analyze each version of python end get his binary."""
        binaries = [Binary(version) for version in versions]
        self.found_versions = []
        self.bad_versions = []
        sorted_binaries = sorted(binaries, key=methodcaller('version'))
        groupped_version_iterator = groupby(sorted_binaries,
                                            key=methodcaller('version'))
        for str_python_ver, bins_iterator in groupped_version_iterator:
            python_version = PythonVersion(version=str_python_ver,
                                           binaries=set(bin_inst.path
                                                        for bin_inst
                                                        in bins_iterator))
            if str_python_ver == 'Unknown':
                self.bad_versions.append(python_version)
            else:
                self.found_versions.append(python_version)
        return self.found_versions


class PythonVersion(object):  # pylint: disable=too-few-public-methods
    """Represent python version which was found."""

    def __init__(self, version, binaries):
        # type: (str, List[Binary]) -> None
        """Python Version constructor."""
        self.version = version
        self.binaries = binaries
