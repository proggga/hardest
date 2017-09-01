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
from typing import Optional  # noqa pylint: disable=unused-import
from typing import Any       # noqa pylint: disable=unused-import
from typing import Iterable  # noqa pylint: disable=unused-import

from hardest.binary import Binary  # noqa pylint: disable=unused-import
from hardest.binary_validator import BinaryValidator
from hardest.interfaces.validator import Validator
from hardest.python_version import PythonVersion


class PythonSearcher(object):
    """Seach Python version for you."""

    python_implementations = (
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
            self.validator = BinaryValidator()  # type: Validator
        elif not isinstance(validator, Validator):
            raise TypeError('Validator is not inherited '
                            'from "Validator" interface.')
        else:
            self.validator = validator
        if not env:
            self.env = os.environ.copy()
        else:
            self.env = env

        self.found_versions = []  # type: List[PythonVersion]
        self.bad_versions = []  # type: List[PythonVersion]

    def search(self):
        # type: () -> Dict[str, List[PythonVersion]]
        """Search python versino and return list of versions."""
        files = self.get_files_from_env()  # type: List[str]
        valid_files = self.get_validated_files(files)  # type: List[str]
        shortnames_list = {}  # type: Dict[str, List[PythonVersion]]
        shortnames_list = PythonVersion.get_binaries(valid_files)
        return shortnames_list

    def get_files_from_env(self):  # pylint: disable=no-self-use
        # type: () -> List[str]
        """Retrun files from system by env PATH var."""
        found_files = []  # type: List[str]
        path_variable = os.environ.get('PATH', '')
        if path_variable:
            dir_list = [os.path.realpath(dirname) for dirname
                        in path_variable.split(':')
                        if os.path.exists(dirname)]
            for dirname in dir_list:
                for filename in os.listdir(dirname):
                    filepath = ''  # type: str
                    filepath = self._check_for_valid(dirname,
                                                     filename)
                    if filepath:
                        found_files.append(filepath)
        return found_files

    def get_validated_files(self, files):  # pylint: disable=no-self-use
        # type: (Iterable[str]) -> List[str]
        """Retrun files which valid by validator."""
        valid_files = list(files)  # type: List[str]
        return valid_files

    def get_valid_files(self, version_to_search):  # pragma: no cover
        # type: (str) -> Set[str]
        """Get binaries path for python versions."""
        whereis_bin = '/usr/bin/whereis'
        command = ['which', 'whereis']  # type: List[str]
        raw_output = check_output(command, env=self.env)  # type: bytes
        decoded_output = str(raw_output.decode())  # type: str
        output = decoded_output.strip()

        if output != whereis_bin:
            whereis_bin = output  # pragma: no cover

        command = [whereis_bin, version_to_search]
        raw_output = check_output(command, env=self.env)
        decoded_output = str(raw_output.decode())
        front_unattended_str = '{}:'.format(version_to_search)
        cropped_output = decoded_output.replace(front_unattended_str, '')
        output = cropped_output.strip()
        files_set = set()  # type: Set[str]
        files_set.add(sys.executable)
        if output:
            files_set |= set(output.split(' '))
        valid_paths = set(filepath for filepath in files_set
                          if self.validator.validate(filepath))
        valid_paths |= self._search_vars_in_path(valid_paths,
                                                 version_to_search)
        return valid_paths

    def _search_vars_in_path(self,
                             already_found=None,  # type: Optional[Set[str]]
                             version_to_search=None,  # type: Optional[str]
                            ):  # noqa # pragma: no cover
        # type: (...) -> Set[str]
        if not version_to_search:
            version_to_search = ''
        if not already_found:
            already_found = set()

        path = self.env.get('PATH', '')  # type: str
        directories = set(path.split(':'))  # type: Set[str]
        dir_names = set()  # type: Set[str]
        dir_names = {os.path.dirname(fil) for fil in already_found}
        directories.difference_update(dir_names)
        files = self._parse_dirs(directories, version_to_search)
        return files

    def _parse_dirs(self, dirs, version_to_search):  # pragma: no cover
        # type: (Set[str], str) -> Set[str]
        files = set()  # type: Set[str]
        for directory in dirs:
            directory = os.path.realpath(directory)
            if not os.path.exists(directory):
                continue

            for filename in os.listdir(directory):
                filepath = ''  # type: str
                filepath = self._check_for_valid(directory,
                                                 filename,
                                                 version_to_search)
                if filepath:
                    files.add(filepath)
        return files

    def _check_for_valid(self, directory, filename,
                         version_to_search=None):  # pragma: no cover
        # type: (str, str, Optional[str]) -> str
        """Check if we search for it and it's valid."""
        versions = []
        if version_to_search:
            versions.append(version_to_search)
        else:
            versions.extend(self.python_implementations)
        filepath = os.path.join(directory, filename)
        searching = [searchword in filename
                     for searchword in versions]
        if any(searching) and self.validator.validate(filepath):
            return filepath
        return ''

    def get_python_versions(self, versions):  # pragma: no cover
        # type: (Union[List[str], Set[str]]) -> List[PythonVersion]
        """Analyze each version of python end get his binary."""
        self.found_versions = []  # type: List[PythonVersion]
        self.bad_versions = []    # type: List[PythonVersion]
        get_version = methodcaller('version')  # type: Callable[[Binary], str]

        binaries = []  # type: List[Binary]
        binaries = [Binary(version) for version in versions]
        sorted_binaries = sorted(binaries, key=get_version)
        grouped_versions = groupby(sorted_binaries,
                                   key=get_version)
        for str_python_ver, bins_iterator in grouped_versions:
            python_version = PythonVersion(version=str_python_ver,
                                           binaries=set(bin_inst.path
                                                        for bin_inst
                                                        in bins_iterator))
            if str_python_ver in ('Unknown', 'Error'):
                self.bad_versions.append(python_version)
            else:
                self.found_versions.append(python_version)
        return self.found_versions
