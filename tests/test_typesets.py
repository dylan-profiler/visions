# TODO: implement tests
import pytest

from tenzing.core.model import tenzing_complete_set
from tenzing.core.model.types import tenzing_float, tenzing_integer, missing_generic, tenzing_generic
from tenzing.core.models import MultiModel


@pytest.fixture(scope='class')
def typeset():
    return tenzing_complete_set()


def test_multi_model_2():
    # All types at same level
    # a + b -> Partitioner(a,b)
    assert isinstance(tenzing_integer + tenzing_float, MultiModel)


def test_multi_model_3():
    # All types at same level
    # a + b + c -> Partitioner (a,b,c)
    assert isinstance(tenzing_integer + tenzing_float + missing_generic, MultiModel)


def test_same_model_2():
    # Identical types
    # a + b + a -> Error
    with pytest.raises(Exception):
        tenzing_integer + tenzing_integer


def test_same_model_3():
    # Identical types
    # a + a -> Error
    with pytest.raises(Exception):
        tenzing_integer + tenzing_float + tenzing_integer


def test_subtype_model():
    # Other level
    # a + child(a) -> Error
    with pytest.raises(Exception):
        tenzing_generic + tenzing_integer
