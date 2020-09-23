from functools import singledispatch
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def string_to_float(sequence: Iterable, state: dict) -> bool:
    return map(str, sequence)


@singledispatch
def string_is_float(sequence: Iterable, state: dict) -> bool:
    return all(float(value) for value in sequence)


@singledispatch
def complex_to_float(sequence: Iterable, state: dict) -> Iterable:
    return map(float, sequence)


@singledispatch
def complex_is_float(sequence: Iterable, state: dict) -> bool:
    return all(value.imag == 0 for value in sequence)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Complex, Generic, String

    relations = [
        IdentityRelation(cls, Generic),
        InferenceRelation(
            cls, String, relationship=string_is_float, transformer=string_to_float
        ),
        InferenceRelation(
            cls,
            Complex,
            relationship=complex_is_float,
            transformer=complex_to_float,
        ),
    ]
    return relations


@singledispatch
def float_contains(sequence: Iterable, state: dict) -> bool:
    return all(isinstance(value, float) for value in sequence)


class Float(VisionsBaseType):
    """**Float** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([1.0, 2.5, 5.0, np.nan])
        >>> x in visions.Float
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return float_contains(sequence, state)
