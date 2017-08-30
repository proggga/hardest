"""Python version class."""
import os

from typing import Set       # noqa pylint: disable=unused-import
from typing import List      # noqa pylint: disable=unused-import
from typing import Dict      # noqa pylint: disable=unused-import
from typing import Iterable  # noqa pylint: disable=unused-import

from hardest.binary import Binary


class PythonVersion(object):  # pylint: disable=too-few-public-methods
    """Represent python version which was found."""

    _versions = []  # type: List[PythonVersion]
    _table = {}  # type: Dict[str, PythonVersion]

    @staticmethod
    def get_version(binary_path):
        # type: (str) -> PythonVersion
        """Create new version or return existing one."""
        if not os.path.exists(binary_path):
            raise OSError('Binary {} does not exists in file system'
                          .format(binary_path))
        table = PythonVersion._table
        versions = PythonVersion._versions

        if binary_path in table:
            return table[binary_path]

        binary = Binary(binary_path)  # type: Binary
        text_version = binary.version()  # type: str

        if text_version in table:
            version = table[text_version]  # type: PythonVersion
            if binary_path not in version.binaries:
                table[binary_path] = version
                version.binaries.add(binary_path)
            return version

        version = PythonVersion(text_version, [binary_path])
        versions.append(version)
        table[text_version] = version
        table[binary_path] = version
        return version

    def __init__(self, version, binaries):
        # type: (str, Iterable[str]) -> None
        """Python Version constructor."""
        self.version = version  # type: str
        self.binaries = set(binaries)  # type: Set[str]

    def __eq__(self, second_addend):
        # type: (object) -> bool
        """Test equality of two pythonversions."""
        if not isinstance(second_addend, PythonVersion):
            return False
        first_addend = self  # type : PythonVersion
        equal_version = bool(first_addend.version == second_addend.version)
        equal_binaries = bool(first_addend.binaries == second_addend.binaries)
        return equal_version and equal_binaries

    def __ne__(self, second_addend):
        # type: (object) -> bool
        """Test not equality of two pythonversions."""
        return not bool(self == second_addend)

    def __hash__(self):
        # type: () -> int
        """Return hash."""
        hash_result = hash(self.version)
        for binary in sorted(self.binaries):
            hash_result ^= hash(binary)
        return hash_result

    def __repr__(self):
        # type: () -> str
        """Class representation."""
        return "PythonVersion object: {} ({})".format(self.version,
                                                      str(self.binaries))

    def __str__(self):
        # type: () -> str
        """Return string representation."""
        return "v: {} ({})".format(self.version,
                                   str(self.binaries))
