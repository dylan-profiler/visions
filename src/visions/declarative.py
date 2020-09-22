from typing import List, Callable, Type, Optional
from visions import VisionsBaseType
from visions.relations import IdentityRelation, TypeRelation


def create_type(
    name : str,
    identity: Type[VisionsBaseType],
    contains: Callable,
    inference: Optional[List[TypeRelation]] = None,
):
    relations = [IdentityRelation(related_type=identity)]
    if inference is not None:
        relations += inference

    def get_relations(cls):
        return relations

    def contains_op(cls, series):
        return contains(series)

    return type(
        name,
        (VisionsBaseType,),
        {
            "get_relations": classmethod(get_relations),
            "contains_op": classmethod(contains_op),
        },
    )


