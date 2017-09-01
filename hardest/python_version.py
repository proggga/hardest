"""Python version class."""
import os

from typing import Set       # noqa pylint: disable=unused-import
from typing import List      # noqa pylint: disable=unused-import
from typing import Dict      # noqa pylint: disable=unused-import
from typing import Iterable  # noqa pylint: disable=unused-import
from typing import Type      # noqa pylint: disable=unused-import

from hardest.binary import Binary


class InvalidFileException(Exception):
    """Invalid File."""


class PythonVersion(object):  # pylint: disable=too-few-public-methods
    """Represent python version which was found."""

    _versions = []  # type: List[PythonVersion]
    _references = {}  # type: Dict[str, PythonVersion]
    _executable = {}  # type: Dict[str, List[PythonVersion]]

    @staticmethod
    def get_versions():
        # type: () -> List[PythonVersion]
        """Get List of versions."""
        return list(PythonVersion._versions)

    @staticmethod
    def get_binaries(valid_files):
        # type: (Iterable[str]) -> Dict[str, List[PythonVersion]]
        """Get dict of versions groupped by binary."""
        PythonVersion.collect_version_data(valid_files)
        return dict(PythonVersion._executable)

    @staticmethod
    def collect_version_data(valid_files_list):
        # type: (Iterable[str]) -> None
        """Retrun files which valid by validator."""
        versions = set()  # type: Set[PythonVersion]
        for file_path in valid_files_list:
            try:
                version = PythonVersion.get_version(file_path)
            except OSError:  # type: ignore
                # File not found, but we continue
                continue
            except InvalidFileException:  # type: ignore
                # file not have valid version
                continue
            versions.add(version)

    @staticmethod
    def get_version(binary_path):
        # type: (str) -> PythonVersion
        """Create new version or return existing one."""
        # if not os.path.exists(binary_path):
        #     raise OSError('Binary {} does not exists in file system'
        #                   .format(binary_path))
        refernces = PythonVersion._references
        versions = PythonVersion._versions

        if binary_path in refernces:
            return refernces[binary_path]

        binary = Binary(binary_path)  # type: Binary
        text_version = binary.version()  # type: str
        if text_version in ('Unknown', 'Error'):
            raise InvalidFileException()
        bin_exec = binary.executable

        if text_version in refernces:
            version = refernces[text_version]  # type: PythonVersion
            PythonVersion.append_new_version(bin_exec, version)
            if binary_path not in version.binaries:
                refernces[binary_path] = version
                version.binaries.append(binary_path)
            return version

        version = PythonVersion(text_version, [binary_path])
        versions.append(version)
        refernces[text_version] = version
        refernces[binary_path] = version
        PythonVersion.append_new_version(bin_exec, version)
        return version

    @staticmethod
    def append_new_version(binary, version):
        # type: (str, PythonVersion) -> None
        """Append version to executable_list."""
        executable_list = PythonVersion._executable
        bin_basename = os.path.basename(binary)
        if bin_basename not in executable_list:
            executable_list[bin_basename] = []
            bin_instance = Binary(bin_basename)
            if bin_instance.version() not in ('Error', 'Unknown'):
                PythonVersion.get_version(bin_instance.path)
        if version not in executable_list[bin_basename]:
            executable_list[bin_basename].append(version)

    def __init__(self, version, binaries):
        # type: (str, Iterable[str]) -> None
        """Python Version constructor."""
        self.version = version  # type: str
        self.binaries = list(sorted(binaries))  # type: List[str]

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
