from pathlib import Path
import pandas as pd

from visions.core.model.model_relation import relation_conf
from visions.core.model.type import VisionsBaseType


class visions_existing_path(VisionsBaseType):
    """**Existing Path** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([Path('/home/user/file.txt'), Path('/home/user/test2.txt')])
        >>> x in visions_existing_path
        True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.implementations.types import visions_path

        relations = {visions_path: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(isinstance(p, Path) and p.exists() for p in series)
