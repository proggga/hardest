"""Module represent PythonSearcher search python binary.

This class helps find available python binary
versions for executing and returns data with version and
binaries.
"""
import os

from collections import OrderedDict

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
        if validator is None:
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

    def search(self):
        # type: () -> Dict[str, List[str]]
        """Search python versino and return list of versions."""
        valid_files = self.get_files_from_env()        # type: List[str]
        result = self.get_default_binaries(valid_files)
        return result

    def get_default_binaries(self, files_list):
        # type (Dict[str, str]) -> Dict[str, str]
        """Return binaries for valid file path."""
        result = {}
        for filename, fullpaths in files_list.items():
            for filepath in fullpaths:
                binary = Binary(filepath, env=self.env)
                if binary.version() in ('Unknown', 'Error'):
                    continue
                try:
                    if binary not in result[filename]:
                        result[filename].append(binary)
                except KeyError:
                    result[filename] = []
                    default_binary = Binary(filename, env=self.env)
                    if (default_binary.version() not in
                            ('Unknown', 'Error')):
                        result[filename].append(default_binary)
                    if binary != default_binary:
                        result[filename].append(binary)
        return result

    def _valid_filename_in(self, dirname):
        def _valid_filename(filename):
            return bool(self._check_for_valid(dirname, filename))
        return _valid_filename

    def get_files_from_env(self):  # pylint: disable=no-self-use
        # type: () -> List[str]
        """Retrun files from system by env PATH var."""
        result_files = OrderedDict()  # type: List[str]
        path_variable = self.env.get('PATH', '')
        if path_variable:
            filtered_dirs = filter(os.path.exists,
                                   path_variable.split(':'))
            dir_list = [os.path.realpath(dirname) for dirname
                        in filtered_dirs]
            for dirname in dir_list:
                file_filter = self._valid_filename_in(dirname)
                filtered_files = filter(file_filter, os.listdir(dirname))
                for filename in filtered_files:
                    filepath = os.path.join(dirname, filename)
                    try:
                        result_files[filename].add(filepath)
                    except KeyError:
                        result_files[filename] = set([filepath])
        return result_files

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
