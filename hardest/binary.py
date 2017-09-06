"""Binary class."""
import os
from subprocess import CalledProcessError
from subprocess import check_output
from subprocess import STDOUT


class Binary(object):  # pylint: disable=too-few-public-methods
    """Represent Binary structure."""

    def __init__(self, path, env=None):
        # type: (str) -> None
        """Binary constructor."""
        self.env = env
        self.executable = os.path.basename(path)  # type: str
        self.path = path                          # type: str
        self._version = ''                        # type: str

    def version(self):
        # type: () -> str
        """Return version, by trying to get from binary."""
        if not self._version:
            version = self._get_version()
            self._version = version
            if version not in ('Unknown', 'Error'):
                self._update_path()
        return self._version

    def _update_path(self):
        # type: () -> None
        """GetPath."""
        binary_output = b''  # type: bytes
        try:
            argx = [self.path,
                    '-c',
                    'import sys; print(sys.executable)']
            binary_output = check_output(argx, stderr=STDOUT, env=self.env)
        except CalledProcessError:
            return
        except OSError:  # type: ignore
            return
        new_path = str(binary_output.decode()).strip()
        if new_path and self.path != new_path and os.path.exists(new_path):
            self.path = new_path

    def _get_version(self):
        # type: () -> str
        raw_result = b''  # type: bytes
        try:
            raw_result = check_output([self.path, '-V'],
                                      stderr=STDOUT, env=self.env)
        except CalledProcessError:
            return 'Unknown'
        except OSError:  # type: ignore
            return 'Error'

        decoded_result = str(raw_result.decode())  # type: str
        if not decoded_result:
            return 'Unknown'

        stripped_version = decoded_result.strip()
        result = stripped_version.replace('\n', ' ')
        return result

    def __eq__(self, second_addend):
        # type: (object) -> bool
        """Test equality of two binaries."""
        if not isinstance(second_addend, Binary):
            return False
        first_addend = self  # type : Binary
        equal_path = bool(first_addend.path == second_addend.path)
        equal_version = bool(first_addend.version() == second_addend.version())
        return equal_path and equal_version

    def __ne__(self, second_addend):
        # type: (object) -> bool
        """Test not equality of two binaries."""
        return not bool(self == second_addend)

    def __hash__(self):
        # type: () -> int
        """Return hash."""
        return hash(self.path) ^ hash(self.version())

    def __repr__(self):
        # type: () -> str
        """Return object representation."""
        return "Binary obj ({}, {})".format(self.path, self.version())

    def __str__(self):
        # type: () -> str
        """Return string representation."""
        return "{} ({})".format(self.path, self.version())
