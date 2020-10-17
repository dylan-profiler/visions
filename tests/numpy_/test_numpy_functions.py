import numpy as np

from visions.backends.numpy.types.integer import (
    float_is_integer,
    float_to_integer,
    integer_contains,
)


def test_sequences():
    assert (
        float_to_integer(np.array([1.0, 2.0, 3.0]), {}) == np.array([1, 2, 3])
    ).all()
    assert float_is_integer(np.array([1.0, 2.0, 3.0]), {})
    assert not float_is_integer(np.array([1.2, 2.0, 3.0]), {})
    assert integer_contains(np.array([1, 2, 3]), {})
    assert not integer_contains(np.array([], dtype=np.int8), {})
    assert not integer_contains(np.array([1.2, 2.3]), {})
