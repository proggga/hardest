"""Module represent PythonSearcher search python binary.

This class helps find available python binary
versions for executing and returns data with version and
binaries.
"""
import os

# For Mypy typing
from typing import List  # noqa pylint: disable=unused-import
from typing import Dict  # noqa pylint: disable=unused-import

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
    )

    def __init__(self):
        pass

    def search(self):
        """Search python versino and return list of versions."""
        # type () -> List[PythonVersion]
        return self.python_search_list


class PythonVersion(object):  # pylint: disable=too-few-public-methods
    """Represent python version which was found."""

    def __init__(self, version, binaries):
        # type: (str, List[Binary])
        self.version = version
        self.binaries = binaries


class Binary(object):  # pylint: disable=too-few-public-methods
    """Represent Binary structure."""

    def __init__(self, path):
        self.executable = os.path.basename(path)
        self.path = path
