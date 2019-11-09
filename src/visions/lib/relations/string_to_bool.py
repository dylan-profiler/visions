from typing import List, Dict


def get_boolean_coercions(id: str) -> List[Dict]:
    coercion_map = {
        "default": [{"true": True, "false": False}],
        "en": [
            {"true": True, "false": False},
            {"y": True, "n": False},
            {"yes": True, "no": False},
        ],
        "nl": [
            {"true": True, "false": False},
            {"ja": True, "nee": False},
            {"j": True, "n": False},
        ],
    }
    return coercion_map[id]


def get_language_bool(language_code: str):
    from visions.core.implementations.types.visions_bool import visions_bool

    return visions_bool.make_string_coercion(
        language_code, get_boolean_coercions(language_code)
    )
