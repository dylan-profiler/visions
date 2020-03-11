from ipaddress import _BaseAddress, ip_address
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types import VisionsBaseType
from visions.utils.coercion import test_utils


def to_ip(series: pd.Series) -> pd.Series:
    return series.apply(ip_address)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Object, String

    relations = [
        IdentityRelation(cls, Object),
        InferenceRelation(
            cls, String, relationship=test_utils.coercion_test(to_ip), transformer=to_ip
        ),
    ]
    return relations


class IPAddress(VisionsBaseType):
    """**IP Address** (v4 and v6) implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> from ipaddress import IPv4Address
        >>> x = pd.Series([IPv4Address('127.0.0.1'), IPv4Address('128.0.1.2')])
        >>> x in visions.IPAddress
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(isinstance(x, _BaseAddress) for x in series)
