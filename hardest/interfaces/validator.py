"""Validator interface."""
import abc

from typing import Any  # noqa # pylint: disable=unused-import

import six


@six.add_metaclass(abc.ABCMeta)  # pylint: disable=R0903,W0232
class Validator(object):
    # disabled checks for pylint
    # R0903 - :too-few-public-methods
    # W0232 - :no-init
    """Validator Interface."""

    @abc.abstractmethod
    def validate(self, data):
        # type: (object) -> bool
        """Validate data and return True or False."""
