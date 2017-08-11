"""
Hardcore test tool module.

Architecture:

+----------+         +-----------+
|   CLI    | ----- > | Templator |
+----------+         +-----------+
      |                     |
     \|/                   \|/
+-----------------+   +----------+
| python_searcher |   | Template |
+-----------------+   +----------+       
         |
        \|/
    +--------+
    | Binary |
    +--------+

"""
from hardest.template import Template
from hardest.templator import Templator

__all__ = ['Templator', 'Template']
