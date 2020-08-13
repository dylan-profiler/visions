import pandas as pd

from visions.typesets import CompleteSet


def test_cast_copy():
    s = pd.Series(["1", "2", "3", "4"])
    id_s = hex(id(s))

    typeset = CompleteSet()
    ns = typeset.cast_to_inferred(s)
    id_ns = hex(id(ns))
    assert id_s != id_ns


def test_noncast_noncopy():
    s = pd.Series(["asdasd", "asdasda", "asdasd", "sadasd"])
    id_s = hex(id(s))

    typeset = CompleteSet()
    ns = typeset.cast_to_detected(s)
    id_ns = hex(id(ns))
    assert id_s == id_ns
