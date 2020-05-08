from typing import Sequence

import pandas as pd
import attr

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types import VisionsBaseType
from visions.utils.coercion import test_utils
from visions.utils.series_utils import nullable_series_contains


def str_to_email(s):
    if isinstance(s, str):
        return FQDA(*s.split("@", maxsplit=1))
    return None


def to_email(series: pd.Series) -> pd.Series:
    return series.apply(str_to_email)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Object, String

    relations = [
        IdentityRelation(cls, Object),
        InferenceRelation(
            cls, String, relationship=test_utils.coercion_test(to_email), transformer=to_email
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
        >>> x = pd.Series([FQDA('example@gmail.com'), FQDA('example@protonmail.com')])
        >>> x in visions.EmailAddress
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @nullable_series_contains
    def contains_op(cls, series: pd.Series) -> bool:
        return all(
            isinstance(x, FQDA) and all((x.local, x.fqdn)) for x in series
        )
