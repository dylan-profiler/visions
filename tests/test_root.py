import pytest

from visions import Float, Generic, VisionsTypeset


class CustomGeneric(Generic):
    this_value = True


class CustomNonGeneric:
    another_value = False


def test_root_node():
    class CustomSet(VisionsTypeset):
        def __init__(self):
            super().__init__({Float}, root_node=CustomGeneric)

    _ = CustomSet()


def test_root_node_other():
    class CustomSet(VisionsTypeset):
        def __init__(self):
            super().__init__({Float}, root_node=CustomNonGeneric)

    with pytest.raises(ValueError, match="`root_node` should be a subclass of Generic"):
        _ = CustomSet()
