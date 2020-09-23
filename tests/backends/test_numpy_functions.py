import numpy as np

from visions.types.integer import float_is_int, integer_contains, to_int


def test_sequences():
    assert (to_int(np.array([1.0, 2.0, 3.0]), {}) == np.array([1, 2, 3])).all()
    assert float_is_int(np.array([1.0, 2.0, 3.0]), {})
    assert not float_is_int(np.array([1.2, 2.0, 3.0]), {})
    assert integer_contains(np.array([1, 2, 3]), {})
    assert not integer_contains(np.array([], dtype=np.int8), {})
    assert not integer_contains(np.array([1.2, 2.3]), {})
