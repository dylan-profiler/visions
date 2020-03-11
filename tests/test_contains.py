import pytest

from tests.series import get_series, get_contains_map


def all_series_included(series_list, series_map):
    """Check that all names are indeed used"""
    used_names = set([name for names in series_map.values() for name in names])
    names = set([series.name for series in series_list])
    if not names == used_names:
        raise ValueError(
            "Not all series are used {unused}".format(unused=names ^ used_names)
        )


def pytest_generate_tests(metafunc):
    _test_suite = get_series()
    if metafunc.function.__name__ == "test_contains":
        _series_map = get_contains_map()

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

        metafunc.parametrize(
            argnames=["series", "type", "member"], argvalues=argsvalues
        )


def test_contains(series, type, member):
    assert member == (series in type)
