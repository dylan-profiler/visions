from typing import Callable
from visions import String
from visions.relations.relations import InferenceRelation
import pandas as pd


def _relationship(series: pd.series, state: dict) -> bool:
    return (series.nunique() / len(series)) < 0.5


def _transformer(series: pd.Series, state: dict) -> bool:
    return series.astype("category")


def string_to_categorical_distinct_count(cls) -> InferenceRelation:
    """Convert string to categorical when it has fewer than 50% unique values.

    Returns:
        relation
    """
    # TODO: only when not any other string relation (either exclude others or have ordering and evaluate last)
    return InferenceRelation(
        relationship=_relationship,
        transformer=_transformer,
        related_type=String,
        type=cls,
    )
