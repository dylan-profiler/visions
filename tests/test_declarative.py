import numpy as np

from visions import Generic, VisionsTypeset
from visions.declarative import create_type


def is_np_float(array, state):
    return np.issubdtype(array.dtype, np.float)


def is_np_int(array, state):
    return np.issubdtype(array.dtype, np.int)


def float_is_int(array, state):
    try:
        return (array.astype(int) == array).all()
    except:
        return False


def to_int(array, state):
    return array.astype(int)


def test_declarative():
    Float = create_type(
        "Float",
        identity=Generic,
        contains=is_np_float,
    )

    Integer = create_type(
        "Integer",
        identity=Generic,
        contains=is_np_int,
        inference=dict(
            related_type=Float, relationship=float_is_int, transformer=to_int
        ),
    )

    my_typeset = VisionsTypeset({Generic, Integer, Float})

    array = np.arange(1, 100).astype(np.float)
    assert my_typeset.detect_type(array) == Float
    assert my_typeset.infer_type(array) == Integer
