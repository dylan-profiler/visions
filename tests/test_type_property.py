from visions import Integer, IPAddress, VisionsBaseType
from visions.relations import TypeRelation


def test_property_base():
    """Assert that _relations is initialized"""
    assert VisionsBaseType._relations is None


def test_property_types():
    """Assert that the relations property contains a list"""
    assert type(Integer.relations) == list and all(
        isinstance(r, TypeRelation) for r in Integer.relations
    )
    assert type(IPAddress.relations) == list and all(
        isinstance(r, TypeRelation) for r in IPAddress.relations
    )
