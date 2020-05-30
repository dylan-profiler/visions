from typing import Sequence, Callable

import pandas as pd
import pytest

from tests.series import get_series


def all_series_included(series_list, series_map):
    """Check that all names are indeed used"""
    used_names = set([name for names in series_map.values() for name in names])
    names = set([series.name for series in series_list])
    if not names == used_names:
        raise ValueError(
            "Not all series are included {unused}".format(unused=names ^ used_names)
        )


def get_contains_cases(mapping: Callable) -> Sequence[pd.Series]:
    _series_map = mapping()
    _test_suite = get_series()

    all_series_included(_test_suite, _series_map)

    argsvalues = []
    for item in _test_suite:
        for type, series_list in _series_map.items():
            args = {
                "id": "{item_name} x {item_type}".format(
                    item_name=item.name, item_type=type
                )
            }

            member = item.name in series_list
            argsvalues.append(pytest.param(item, type, member, **args))

    return argsvalues


def contains(member, series, type):
    return member == (
        series in type
    ), f"{series.name} in {type}; expected {member}, got {series in type}"