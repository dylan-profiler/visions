from importlib import util as import_util


def has_import(module: str) -> bool:
    has_module = import_util.find_spec(module) is not None
    return has_module
