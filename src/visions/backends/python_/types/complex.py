from typing import Iterable

from visions.types.complex import Complex
from visions.types.string import String
from visions.backends.python_.series_utils import sequence_not_empty
from visions.backends.python_.types.float import no_leading_zeros


@Complex.register_relationship(String, Iterable)
def string_is_complex(sequence: Iterable, state: dict) -> bool:
    try:
        coerced = list(string_to_complex(sequence, state))
        return no_leading_zeros(sequence, [r.real for r in coerced])
    except:
        return False


@Complex.register_transformer(String, Iterable)
def string_to_complex(sequence: Iterable, state: dict) -> Iterable:
    return list(map(complex, sequence))


@Complex.contains_op.register(Iterable)
@sequence_not_empty
def complex_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, complex) for value in sequence)
