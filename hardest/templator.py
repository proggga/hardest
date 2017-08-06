"""Templator class which helps render templates."""
from typing import Dict  # noqa pylint: disable=unused-import
from typing import Any  # noqa pylint: disable=unused-import
from typing import Optional  # noqa pylint: disable=unused-import

import os
import pkg_resources

import hardest.exceptions
import hardest.template


class Templator(object):
    """Template generator."""

    def __init__(self, package_name):
        """Init constructor."""
        # type: (str) -> None
        self.package_name = package_name  # type: str

    def get_template(self, template_name, context=None):
        """Render by template_name."""
        # type: (str, Optional[Dict[str, Any]]) -> str
        if not context:
            context = {}
        file_path = self.get_template_path(template_name)
        return hardest.template.Template(file_path, context)

    def get_template_path(self, template_name):
        """Get template path."""
        # type: (str) -> str
        try:
            file_name = pkg_resources.resource_filename(self.package_name,
                                                        template_name)
            if os.path.exists(file_name):
                return file_name
        except ImportError:
            message = ('Package "{}" not found'
                       .format(self.package_name))
            raise hardest.exceptions.TemplateNotFoundException(message)
        message = ('Template "{}" not found in package "{}"'
                   .format(template_name, self.package_name))
        raise hardest.exceptions.TemplateNotFoundException(message)
