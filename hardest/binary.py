"""Binary class."""
import os
from subprocess import check_output
from subprocess import CalledProcessError
from subprocess import STDOUT


class Binary(object):  # pylint: disable=too-few-public-methods
    """Represent Binary structure."""

    def __init__(self, path):
        # type: (str) -> None
        self.executable = os.path.basename(path)  # type: str
        self.path = path                          # type: str
        self._version = ''                        # type: str

    def version(self):
        # type: () -> str
        """Return version, by trying to get from binary."""
        if not self._version:
            print("Exec {}".format(self.path))
            raw_result = b''  # type: bytes
            try:
                raw_result = check_output([self.path, '-V'],
                                          stderr=STDOUT)  # type: ignore
            except CalledProcessError:
                return 'Unknown'

            decoded_result = raw_result.decode()  # type: str
            if not decoded_result:
                return 'Unknown'

            self._version = decoded_result

        return self._version
