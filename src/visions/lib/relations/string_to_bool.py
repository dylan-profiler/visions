from visions.core.model.model_relation import relation_conf
from visions.core.implementations.types import to_bool
from visions.utils.coercion.test_utils import coercion_map_test, coercion_map


def string_to_bool_dutch():
    coercions = [
        {"true": True, "false": False},
        {"y": True, "n": False},
        {"yes": True, "no": False},
        {"ja": True, "nee": False},
        {"j": True, "n": False},
    ]

    return relation_conf(
        inferential=True,
        relationship=lambda s: coercion_map_test(coercions)(s.str.lower()),
        transformer=lambda s: to_bool(coercion_map(coercions)(s.str.lower())),
    )
