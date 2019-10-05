import pandas as pd
from ipaddress import _BaseAddress, ip_address

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model
from tenzing.utils.coercion import test_utils


class tenzing_ip(tenzing_model):
    """**IP Address** (v4 and v6) implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> from ipaddress import IPv4Address
    >>> x = pd.Series([IPv4Address('127.0.0.1'), IPv4Address('128.0.1.2')])
    >>> x in tenzing_ip
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_object, tenzing_string

        relations = {
            tenzing_object: relation_conf(inferential=False),
            tenzing_string: relation_conf(inferential=True, relationship=test_utils.coercion_test(lambda s: s.apply(ip_address))),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(lambda x: isinstance(x, _BaseAddress)).all()

    @classmethod
    def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
        return series.apply(ip_address)
