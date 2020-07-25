"""
Test for issue 85
https://github.com/dylan-profiler/visions/issues/85
"""
import pytest

from visions import VisionsTypeset
from visions.types import *


class ExampleTypeSet(VisionsTypeset):
    """Typeset for testing: String is not included as type, however there are
    types with inference relations from string"""

    def __init__(self):
        types = {
            Generic,
            Categorical,
            Boolean,
            Float,
            DateTime,
            URL,
            Complex,
            Path,
            File,
            Image,
            Integer,
            Object,
        }
        super().__init__(types)


def test_typeset_external_type():
    """When a typeset contains at least one type that has a relation from a type that is not in the typeset:
    - the user should be warned
    - the typeset should not include that type
    - that type should not be present in the graph when printed

    """

    # Expecting warnings to match
    with pytest.warns(UserWarning, match="but String was not included in") as record:
        pp_typeset = ExampleTypeSet()

    # Expecting 6 warnings
    assert len(record) == 6

    assert String not in pp_typeset.types

    assert String not in pp_typeset.relation_graph.nodes
