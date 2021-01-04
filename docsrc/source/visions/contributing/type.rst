Contributions new types to visions
**********************************
``visions`` is a continuously evolving project with the aim of expanding it's set of useful
semantic types. To that end, if you find a type construction useful, please feel free to contribute
it back here.

Below you will find a checklist with instructions on which files to add or modify.

Type implementation:

- place the type implementation in ``src/visions/contrib/types/[your type_name].py``
- include the type in ``src/visions/contrib/types/__init__.py``
- include the type in a relevant typeset, or create one ``src/visions/contrib/typesets/[your_typeset].py``

Tests:

- add tests to ``tests/contrib/typesets/test_[your_typeset].py`` (use one of the other typesets as template).
- optionally add series to ``tests/series.py``

Documentation:

- provide informative docstrings ``src/visions/contrib/types/[your type_name].py``
- include the type in the api documentation: ``docsrc/source/visions/api/types.rst``
- add a row to the defaults table: ``docsrc/source/visions/getting_started/usage/defaults.rst``
