from typing import Callable, List, Optional, Type

from visions import VisionsBaseType
from visions.relations import IdentityRelation, InferenceRelation, TypeRelation


def create_type(
    name: str,
    identity: Type[VisionsBaseType],
    contains: Callable,
    inference: Optional[List[dict]] = None,
):
    def get_relations(cls):
        relations = [IdentityRelation(cls, related_type=identity)]
        if inference is not None:
            relations += [InferenceRelation(cls, **params) for params in inference]

        return relations

    def contains_op(cls, series, state):
        return contains(series, state)

    return type(
        name,
        (VisionsBaseType,),
        {
            "get_relations": classmethod(get_relations),
            "contains_op": classmethod(contains_op),
        },
    )
