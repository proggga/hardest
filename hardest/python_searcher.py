"""Module represent PythonSearcher search python binary.

This class helps find available python binary
versions for executing and returns data with version and
binaries.
"""
import os

# For Mypy typing
from typing import List  # noqa pylint: disable=unused-import
from typing import Union  # noqa pylint: disable=unused-import
from typing import Dict  # noqa pylint: disable=unused-import
from typing import Tuple  # noqa pylint: disable=unused-import

from subprocess import check_output

from hardest.binary import Binary  # noqa pylint: disable=unused-import


class PythonSearcher(object):
    """Seach Python version for you."""

    python_search_list = (
        'python',
        'ironpython',
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
        pass

    def search(self):
        # type: () -> List[PythonVersion]
        """Search python versino and return list of versions."""
        valid_files_list = []  # type: List[str]
        for version_to_search in self.python_search_list:  # type: str
            file_list = self.get_valid_files(version_to_search)
            if not valid_files_list:
                continue
            valid_files_list.extend(file_list)

        founded = []  # type: List[PythonVersion]
        founded = self.get_python_versions(valid_files_list)

        return founded

    def get_valid_files(self, version_to_search):
        # type: (str) -> List[str]
        """Get binaries path for python versions."""
        command = ['whereis', version_to_search]  # type: List[str]
        raw_output = check_output(command)  # type: bytes
        decoded_output = str(raw_output.decode())  # type: str
        front_unattended_str = '{}: '.format(version_to_search)
        cropped_output = decoded_output.replace(front_unattended_str, '')
        output = cropped_output.strip()
        files_list = output.split(' ')
        return [filepath for filepath in files_list
                if self._valid_path(filepath)]

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
        return []


class PythonVersion(object):  # pylint: disable=too-few-public-methods
    """Represent python version which was found."""

    def __init__(self, version, binaries):
        # type: (str, List[Binary]) -> None
        self.version = version
        self.binaries = binaries
