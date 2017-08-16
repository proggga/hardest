"""Binary file validator."""
import os

from hardest.interfaces.validator import Validator


class BinaryValidator(Validator):  # pylint: disable=R0903,W0232
    """Validate is binary file is valid."""

    def validate(self, data):
        # type: (object) -> bool
        """Validate is file is ok."""
        filename = str(data)  # type: str
        return (bool(filename) and
                not filename.endswith('-config') and
                os.path.isfile(filename) and
                not os.path.islink(filename) and
                os.access(filename, os.X_OK))
