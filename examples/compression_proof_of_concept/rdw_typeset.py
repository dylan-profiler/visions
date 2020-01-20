from visions.core.implementations import visions_complete_set
from visions.core.implementations.types import visions_bool

from visions.lib.relations.string_to_bool import get_language_bool
from visions.lib.relations.string_to_ordinal import string_to_ordinal


# make Dutch boolean
visions_bool_nl = get_language_bool("nl")
rdw_typeset = visions_complete_set() + visions_bool_nl
