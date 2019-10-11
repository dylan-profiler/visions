from visions.core.model.model_relation import relation_conf
from visions.utils.monkeypatches import *
import imghdr
from pathlib import Path

import pandas as pd

from visions.core.model.models import tenzing_model


class tenzing_image_path(tenzing_model):
    """**Image Path** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([Path('/home/user/file.png'), Path('/home/user/test2.jpg')])
    >>> x in tenzing_image_path
    True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.model.types import tenzing_existing_path

        relations = {tenzing_existing_path: relation_conf(inferential=False)}
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(isinstance(p, Path) and p.exists() and imghdr.what(p) for p in series)
