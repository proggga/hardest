"""Templator class which helps render templates."""
from typing import Dict  # noqa pylint: disable=unused-import
from typing import Any  # noqa pylint: disable=unused-import
from typing import Optional  # noqa pylint: disable=unused-import

import os
import pkg_resources  # type: ignore

import hardest.exceptions
import hardest.template


class Templator(object):
    """Template generator."""

    def __init__(self, package_name):
        # type: (str) -> None
        self.package_name = package_name  # type: str

    def get_template(self,
                     template_name,  # type: str
                     context=None    # type: Dict[str, Any]
                    ):
        # type: (...) -> hardest.template.Template
        """Render by template_name."""

        if not context:
            context = {}
        file_path = self.get_template_path(template_name)  # type: str
        return hardest.template.Template(file_path, context)

    def get_template_path(self, template_name):
        # type: (str) -> str
        """Get template path."""

        try:
            file_name = ''  # type: str
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
