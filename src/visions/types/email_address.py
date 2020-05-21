from typing import Sequence

import attr
import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.coercion import test_utils
from visions.utils.series_utils import nullable_series_contains


def test_email(series):
    return to_email(series).apply(lambda x: x.local and x.fqdn).all()


def str_to_email(s):
    if isinstance(s, FQDA):
        return s
    elif isinstance(s, str):
        return FQDA(*s.split("@", maxsplit=1))
    else:
        raise TypeError('Only strings supported')


def to_email(series: pd.Series) -> pd.Series:
    return series.apply(str_to_email)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Object, String

    relations = [
        IdentityRelation(cls, Object),
        InferenceRelation(
            cls,
            String,
            relationship=test_utils.coercion_test(test_email),
            transformer=to_email,
        ),
    ]
    return relations


@attr.s(slots=True)
class FQDA(object):
    local = attr.ib()
    fqdn = attr.ib()

    @staticmethod
    def from_str(s):
        return str_to_email(s)


class EmailAddress(VisionsBaseType):
    """**EmailAddress** implementation of :class:`visions.types.type.VisionsBaseType`.

    Notes:
        The email address should be a **fully qualified domain address** (FQDA)
        FQDA = local part + @ + fully qualified domain name (FQDN)
        This type

    Examples:
        >>> x = pd.Series([FQDA('example','gmail.com'), FQDA.from_str('example@protonmail.com')])
        >>> x in visions.EmailAddress
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        # TODO: x.local and x.fqdn for all, isinstance for a sample
        return all(isinstance(x, FQDA) and all((x.local, x.fqdn)) for x in series)
