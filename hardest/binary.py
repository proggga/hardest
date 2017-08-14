"""Binary class."""
import os
from subprocess import CalledProcessError
from subprocess import check_output
from subprocess import STDOUT


class Binary(object):  # pylint: disable=too-few-public-methods
    """Represent Binary structure."""

    def __init__(self, path):
        # type: (str) -> None
        """Binary constructor."""
        self.executable = os.path.basename(path)  # type: str
        self.path = path                          # type: str
        self._version = ''                        # type: str

    def version(self):
        # type: () -> str
        """Return version, by trying to get from binary."""
        if not self._version:
            return self._get_version()
        return self._version

    def _get_version(self):
        # type: () -> str
        raw_result = b''  # type: bytes
        try:
            raw_result = check_output([self.path, '-V'],
                                      stderr=STDOUT)  # type: ignore
        except CalledProcessError:
            return 'Unknown'

        decoded_result = str(raw_result.decode())  # type: str
        if not decoded_result:
            return 'Unknown'

        stripped_version = decoded_result.strip()
        self._version = stripped_version.replace('\n', ' ')
        return self._version
