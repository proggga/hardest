"""Python version class."""


class PythonVersion(object):  # pylint: disable=too-few-public-methods
    """Represent python version which was found."""

    def __init__(self, version, binaries):
        # type: (str, Set[str]) -> None
        """Python Version constructor."""
        self.version = version
        self.binaries = binaries

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
