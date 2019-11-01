from visions.core.model.model_relation import relation_conf
import imghdr
from pathlib import Path

import pandas as pd

from visions.core.model.type import VisionsBaseType


class visions_image_path(VisionsBaseType):
    """**Image Path** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([Path('/home/user/file.png'), Path('/home/user/test2.jpg')])
        >>> x in visions_image_path
        True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.implementations.types import visions_existing_path

        relations = {visions_existing_path: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(
            isinstance(p, Path) and p.exists() and imghdr.what(p) for p in series
        )
