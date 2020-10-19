import numpy as np

from visions import Generic, VisionsTypeset, create_type


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


Float = create_type(
    "Float",
    identity=Generic,
    contains=is_np_float,
)

Integer = create_type(
    "Integer",
    identity=Generic,
    contains=is_np_int,
    inference=dict(related_type=Float, relationship=float_is_int, transformer=to_int),
)

my_typeset = VisionsTypeset({Generic, Integer, Float})
my_typeset.output_graph("declarative_set.pdf")
