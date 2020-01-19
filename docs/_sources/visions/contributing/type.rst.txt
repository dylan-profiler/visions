Contributions new types to visions
**********************************
Your custom type might be helpful for others, in which case you can choose to contribute it to `visions`.
Below you will find a checklist with instructions on which files to add or modify.

Type implementation:

- place the type implementation in `src/visions/core/implementations/types/visions_[your type_name].py`
- include the type in `src/visions/core/implementations/types/__init__.py`
- include the type in a relevant typeset, or create one `src/visions/core/implementations/typesets.py`

Tests:

- add series to `tests/series.py` that test the type
- add series to `tests/series.py` that test the each relation

Documentation:

- provide informative docstrings `src/visions/core/implementations/types/visions_[your type_name].py`
- include the type in the api documentation: `docsrc/source/visions/api/types.rst`
- add a row to the defaults table: `docsrc/source/visions/practitioner/defaults.rst`
