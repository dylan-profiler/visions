import pytest

from tests.series import get_series, get_contains_map


def all_series_included(series_list, series_map):
    """Check that all names are indeed used"""
    used_names = set([name for names in series_map.values() for name in names])
    names = set([series.name for series in series_list])
    if not names == used_names:
        raise ValueError(f"Not all series are used {names ^ used_names}")


def pytest_generate_tests(metafunc):
    _test_suite = get_series()
    if metafunc.function.__name__ == "test_contains":
        _series_map = get_contains_map()

        all_series_included(_test_suite, _series_map)

        argsvalues = []
        for item in _test_suite:
            for type, series_list in _series_map.items():
                args = {"id": f"{item.name} x {type}"}
                if item.name not in series_list:
                    args["marks"] = pytest.mark.xfail(raises=AssertionError)

                argsvalues.append(pytest.param(item, type, **args))

        metafunc.parametrize(argnames=["series", "type"], argvalues=argsvalues)


@pytest.mark.run(order=7)
def test_contains(series, type):
    assert series in type
