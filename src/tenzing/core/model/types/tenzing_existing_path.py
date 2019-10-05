from pathlib import Path
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model


class tenzing_existing_path(tenzing_model):
    """**Existing Path** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
    >>> x in tenzing_existing_path
    True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_path

        relations = {tenzing_path: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return series.apply(lambda p: isinstance(p, Path) and p.exists()).all()
