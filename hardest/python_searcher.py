"""Module represent PythonSearcher search python binary.

This class helps find available python binary
versions for executing and returns data with version and
binaries.
"""
import os
import sys

from itertools import groupby
from operator import methodcaller
from subprocess import check_output

# For Mypy typing
from typing import List      # noqa pylint: disable=unused-import
from typing import Union     # noqa pylint: disable=unused-import
from typing import Dict      # noqa pylint: disable=unused-import
from typing import Tuple     # noqa pylint: disable=unused-import
from typing import Set       # noqa pylint: disable=unused-import
from typing import Callable  # noqa pylint: disable=unused-import
from typing import Any       # noqa pylint: disable=unused-import

from hardest.binary import Binary  # noqa pylint: disable=unused-import
from hardest.binary_validator import BinaryValidator
from hardest.interfaces.validator import Validator


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

    def __init__(self,
                 env=None,  # type: Optional[Dict[str, str]]
                 validator=None  # type: Optional[Validator]
                ):  # noqa
        # type: (...) -> None
        """Searcher constructor."""
        if not validator:
            self.validator = BinaryValidator()
        elif not isinstance(validator, Validator):
            raise TypeError('Validator is not inherited '
                            'from "Validator" interface.')
        else:
            self.validator = validator
        if not env:
            self.env = os.environ.copy()
        else:
            self.env = env

        print('ENV', self.env)
        self.found_versions = []  # type: List[PythonVersion]
        self.bad_versions = []  # type: List[PythonVersion]

    def search(self):
        # type: () -> List[PythonVersion]
        """Search python versino and return list of versions."""
        valid_files_list = set()  # type: Set[str]
        for version_to_search in self.python_search_list:  # type: str
            files = self.get_valid_files(version_to_search)
            print("FILES", files)
            if not files:
                continue
            valid_files_list.update(set(files))
        self.get_python_versions(valid_files_list)

        return self.found_versions

    def get_valid_files(self, version_to_search):
        # type: (str) -> Set[str]
        """Get binaries path for python versions."""
        whereis_bin = '/usr/bin/whereis'
        command = ['which', 'whereis']  # type: List[str]
        raw_output = check_output(command, env=self.env)  # type: bytes
        decoded_output = str(raw_output.decode())  # type: str
        output = decoded_output.strip()

        print('whereis_bin', whereis_bin, os.path.exists(whereis_bin))
        if output != whereis_bin:
            whereis_bin = output  # pragma: no cover

        print('whereis_bin', whereis_bin, os.path.exists(whereis_bin))
        command = [whereis_bin, version_to_search]  # type: List[str]
        raw_output = check_output(command, env=self.env)  # type: bytes
        decoded_output = str(raw_output.decode())  # type: str
        front_unattended_str = '{}:'.format(version_to_search)
        cropped_output = decoded_output.replace(front_unattended_str, '')
        output = cropped_output.strip()
        files_set = set()  # type: Set[str]
        if not output:
            return files_set
        files_set |= set(output.split(' '))
        files_set.add(sys.executable)
        valid_paths = set(filepath for filepath in files_set
                          if self.validator.validate(filepath))
        return valid_paths

    def get_python_versions(self, versions):
        # type: (Union[List[str], Set[str]]) -> List[PythonVersion]
        """Analyze each version of python end get his binary."""
        self.found_versions = []  # type: List[PythonVersion]
        self.bad_versions = []    # type: List[PythonVersion]
        get_version = methodcaller('version')  # type: Callable[[Binary], str]

        binaries = []  # type: List[Binary]
        print(versions)
        binaries = [Binary(version) for version in versions]
        sorted_binaries = sorted(binaries, key=get_version)
        grouped_versions = groupby(sorted_binaries,
                                   key=get_version)
        for str_python_ver, bins_iterator in grouped_versions:
            python_version = PythonVersion(version=str_python_ver,
                                           binaries=set(bin_inst.path
                                                        for bin_inst
                                                        in bins_iterator))
            print(python_version.version, python_version.binaries)
            if str_python_ver == 'Unknown':
                self.bad_versions.append(python_version)
            else:
                self.found_versions.append(python_version)
        return self.found_versions


class PythonVersion(object):  # pylint: disable=too-few-public-methods
    """Represent python version which was found."""

    def __init__(self, version, binaries):
        # type: (str, Set[str]) -> None
        """Python Version constructor."""
        self.version = version
        self.binaries = binaries
