Data Validation
===============

Data validation is intended to provide automated guarantees over the input data, validating whether the data are meaningful, correct, accurate, consistent or complete.
In data analysis, we often expect certain assumption to be invariant over time regardless of how the dataset is manipulated.
For example, we might expect a field to always be unique (identifier) or a number to range between one and five (ratings).
Tight coupling causes the same problem as discussed above because the user often designs validation rules that are grounded in the meaning of the data.

A variety of software packages have been developed to facilitate this workflow [#f1]_, [#f2]_, [#f3]_, [#f4]_, [#f5]_, [#f6]_.
These packages can benefit from decoupling semantic and machine type representations.

The part of data validation that depends on machine types, the validation methods, should have to focus of such a package.
For example, the software could have helper functions to assert if a float is approximately the reference value (see ``pytest.approx`` in [pytest]_).
The other part, defining and checking properties of the data depends on semantic types.
For example, the International Standard Book Number (ISBN) has a `check digit <https://en.wikipedia.org/wiki/Check_digit>`_, which only makes sense to validate when a stored number is representing the ISBN.
A key observation is that this highly overlaps with the data summarization example discussed above.
Large components of that application can be reused to reduce code complexity.

.. [pytest] pytest x.y, 2004
    Krekel et al., https://github.com/pytest-dev/pytest

.. rubric:: Footnotes

.. [#f1] https://github.com/great-expectations/great_expectations
.. [#f2] https://github.com/zaxr/bulwark
.. [#f3] https://github.com/engarde-dev/engarde
.. [#f4] https://github.com/csparpa/fluentcheck
.. [#f5] https://github.com/jmenglund/pandas-validation
.. [#f6] https://github.com/TMiguelT/PandasSchema