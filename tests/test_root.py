import pytest

from visions import Generic, VisionsBaseType, VisionsTypeset
from visions.relations import IdentityRelation


class CustomGeneric(Generic):
    this_value = True


class CustomNonGeneric(VisionsBaseType):
    another_value = False

    @classmethod
    def get_relations(cls):
        return []


def make_test_type(root):
    class CustomFloat(VisionsBaseType):
        @classmethod
        def contains_op(cls, series):
            return True

        @classmethod
        def get_relations(cls):
            return [IdentityRelation(cls, root)]

    return CustomFloat


def test_root_node():
    class CustomSet(VisionsTypeset):
        def __init__(self):
            super().__init__({make_test_type(CustomGeneric), CustomGeneric})

    _ = CustomSet()


def test_root_node_other():
    class CustomSet(VisionsTypeset):
        def __init__(self):
            super().__init__({make_test_type(CustomNonGeneric), CustomNonGeneric})

    with pytest.raises(ValueError, match="`root_node` should be a subclass of Generic"):
        _ = CustomSet()


def test_multiple_roots():
    class CustomSet(VisionsTypeset):
        def __init__(self):
            super().__init__({make_test_type(CustomGeneric), CustomGeneric, Generic})

    _ = CustomSet()
