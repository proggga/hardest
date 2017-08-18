r"""
Hardcore test tool module.

Class Architecture Scheme:

+----------+         +-----------+
|   CLI    | ----- > | Templator |
+----------+         +-----------+
 |     |                   |
 |    \|/                 \|/
 |  +-------------+   +----------+
 |  | ConfigSaver |   | Template |
 |  +-------------+   +----------+
 |
 |      +-----------------+
 +----> | python_searcher |
        +-----------------+
                |
               \|/
            +--------+
            | Binary |
            +--------+


||    CLI    ||     Templator     ||   Template   ||
||  run -----||--->get_template() ||              ||
||  |        ||     +-------------||-> new()      ||
||  |        ||     |<------------||---+          ||
||  |<-------||---<-+ret template ||   |          ||
||  |        ||                   ||   |          ||
||  ---- execution of part 1 of algorithm ------  ||
||  |<-------||-------------------||--+render(str)||
||  ---- execution of part 2 of algorithm ------  ||


||  -------- part 1 of algorithm -----------  ||
||    CLI    || python_searcher||   Binary    ||
||  |--------||-->search()     ||             ||
||  |        ||  |-------------||->new()      ||
||  |        ||  |<------------||<+-version() ||
||  |<-------||<-+ret List[str]||             ||


||  ---part 2 of algorithm---  ||
||  CLI      ||  ConfigSaver   ||
||  |--------||->save(content) ||


"""
from hardest.template import Template
from hardest.templator import Templator

__all__ = ['Templator', 'Template']
