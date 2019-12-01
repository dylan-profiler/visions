import pandas as pd

from visions.core.model import TypeRelation


def identity_relation(series: pd.Series) -> pd.Series:
    return series


class IdentityRelation(TypeRelation):
    def __init__(self, type, related_type, relationship=None):
        relationship = type.__contains__ if relationship is None else relationship
        super().__init__(
            type,
            related_type,
            relationship=relationship,
            transformer=identity_relation,
            inferential=False,
        )

    def __repr__(self) -> str:
        return f"IdentityRelation({self.related_type} -> {self.type})"


class InferenceRelation(TypeRelation):
    def __init__(self, type, related_type, transformer, relationship=None):
        relationship = type.__contains__ if relationship is None else relationship
        super().__init__(
            type,
            related_type,
            relationship=relationship,
            transformer=transformer,
            inferential=True,
        )

    def __repr__(self) -> str:
        return f"InferenceRelation({self.related_type} -> {self.type})"
