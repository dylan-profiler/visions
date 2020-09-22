Typeset testing
===============

To test a typeset we typically apply it to a collection of series and assess the type that is detected matches the one that is expected. Visions contains a collection of utility functions that can help you test your typeset. Additionally, you can reuse the extensive collection of series that visions uses internally.

The name of the series is used as identifier:

.. code-block:: python

    testable_series = [
        pd.Series([1,2,3], name='numeric_series'),
        pd.Series([1,2,3,np.nan], name='numeric_series_missing'),
    ]

There are currently three kind of test cases that can be automatically generated to easily test the typeset: contains, inference and conversion. The test cases are generated based on an easily defined mapping specific to the type of test.

Testing contains
----------------
Defining your own test cases for the "contains" relation requires a simple mapping from each type to a set of series identifiers. All series in the provided list of series should be included the the mapping. If not, ``get_contains_cases`` will kindly tell you which ones are missing. The example below shows a minimal example.

.. code-block:: python

    import pytest
    from visions.test.series import get_series
    from visions.test.utils import contains, get_contains_cases

    # Mapping from type to series identifier
    typeset = YourTypeset()

    contains_map = {
    	YourType1: {"int_series", "int_range",},
    	YourType2: {"path_series_linux", "path_series_linux_missing", "path_series_windows"},
    	YourType3: {"url_series", "url_nan_series", "url_none_series"},
    	# (...)
    }

    # Generating the test cases
    @pytest.mark.parametrize(**get_contains_cases(contains_map, typeset))
    def test_contains(series, type, member):
        """Test the generated combinations for "series in type"

    	Args:
            series: the series to test
	    type: the type to test against
	    member: the result
        """
        result, message = contains(series, type, member)
        assert result, message


Testing inference and conversion
--------------------------------
For the other tests, please see visions' tests. The directory ``tests/typesets/`` contains visions' own typeset tests. For instance, the ``CompleteSet`` with all default types is tested in ``test_complete_set.py`` and can be used as guiding template.

