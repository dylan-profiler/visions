import pandas as pd

from visions.core.implementations.typesets import visions_complete_set


def test_cast_copy():
    s = pd.Series(["1", "2", "3", "4"])
    id_s = hex(id(s))

    typeset = visions_complete_set()
    ns = typeset.cast_series(s)
    id_ns = hex(id(ns))
    assert id_s != id_ns


def test_noncast_noncopy():
    s = pd.Series(["asdasd", "asdasda", "asdasd", "sadasd"])
    id_s = hex(id(s))

    typeset = visions_complete_set()
    ns = typeset.cast_series(s)
    id_ns = hex(id(ns))
    assert id_s == id_ns
