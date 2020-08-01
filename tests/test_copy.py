import pandas as pd

from visions.typesets import CompleteSet


def test_cast_copy():
    s = pd.Series(["1", "2", "3", "4"])
    id_s = hex(id(s))

    typeset = CompleteSet()
    ns = typeset.infer_and_cast(s)
    id_ns = hex(id(ns))
    assert id_s != id_ns


def test_noncast_noncopy():
    s = pd.Series(["asdasd", "asdasda", "asdasd", "sadasd"])
    id_s = hex(id(s))

    typeset = CompleteSet()
    ns = typeset.cast(s)
    id_ns = hex(id(ns))
    assert id_s == id_ns
