"""Template class."""
import os

# For Mypy typing
from typing import Any  # noqa pylint: disable=unused-import
from typing import Dict  # noqa pylint: disable=unused-import

import hardest.exceptions
import jinja2


class Template(object):  # pylint: disable=too-few-public-methods
    """Represents tepmplate which can be rendered."""

    def __init__(self, file_path, context):
        """Constructor."""
        # type: (str, Dict[str:Any]) -> None
        self.file_path = file_path  # type: str
        self.context = context  # type: Dict[str:Any]

    def render(self):
        """Render template."""
        # type () -> str
        if not os.path.exists(self.file_path):
            message = ('Path "{}" not exists.'
                       .format(self.file_path))
            raise hardest.exceptions.TemplateNotFoundException(message)
        file_handler = open(self.file_path)
        template_content = str(file_handler.read())
        file_handler.close()

        template = jinja2.Template(template_content)
        rendered_content = str(template.render(**self.context))
        return rendered_content
