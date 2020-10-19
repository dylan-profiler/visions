Open challenges
===============

Visions is opinionated, so what are the main opinions?

.. Point, Example, Solution

#1: Don't mix machine and semantic type logic
----------------------------------------------
Example `pandas.read_csv <https://pandas.pydata.org/pandas-docs/version/1.0.0/user_guide/io.html#io-read-csv-table>`_

The pandas.read_csv functionality is an excellent example where machine and semantic type logic is (currently) mixed.
The machine type logic concerns how columns are stored and encoded.
Arguments as ``delimeter``, ``header``, ``nrows``, ``compression`` are related to that.

The semantic type logic is also included: ``thousands``, ``converters``, ``date_parser``, ``dayfirst``.

Our hope: machine and semantic type logic will be decoupled.

note that the pandas docs agree

    We would love to turn this module into a community supported set of date/time parsers.

#2: (Semantic) Data types are not a fixed set
---------------------------------------------
Many libraries appear to believe that data types are a fixed set, and that once common types are supported, work is done.
Semantic type inference depends on the real world context, and can in practice not be automated without user input.

Example: ...

#3: Making a small change to a data type may require hundreds of lines of code
------------------------------------------------------------------------------
Pandas' introduced Extension types in version 0.23.0, which allows users to define custom types [1].
The current state is that adding a type (e.g. ip-address) requires hundreds lines of code.

https://github.com/ContinuumIO/cyberpandas

Our hope: extending will be more user-centric by requiring only the minimum changes.

#4: Semantic logic needs a dedicated module
-------------------------------------------
Currently, python data modules implement their own type inference heuristics.

For example MLBox, a python library for automated machine learning (AutoML) implements heuristics in the reader (in violation of #1).
https://github.com/AxeldeRomblay/MLBox/blob/4ad2f664102c031705d4eda6bf50e27a78bfc96d/mlbox/preprocessing/reader.py
The heuristics contain logic for parsing of datetimes, floats and makes assumptions on what a categorical is.
Moreover, it adds redundancy to program yet another type inference system.

Solution: use a dedicated module for semantic type inference (i.e. ``visions``)

Example:
https://github.com/h2oai/h2o-3/blob/61275cf63d981d332220fa3aef157989fcef3305/h2o-py/h2o/h2o.py#L454



Combating the beliefs that:
- There is no difference between machine and semantic types
- One static typeset is enough for your application
- Not all users have to be able to add types
- We can shortcut types and make ad-hoc implementations
- We don't need a collection of data types (how good is a recipe book without recipes)
- We should cram as much functionality in single packages and solve many complex problems.
- We should mix type logic with other functionality.

A typing framework allows application to uncover hidden tight coupling and reason over types in a productive manner.
This framework can lay a strong foundation for subsequent data-intensive applications.

- Dedicated as opposed to all encompassing
- Flexibility as opposed to intensive implementation:
- Performant as opposed to computationally expensive:
- Explicit as opposed to implicit:

- Serves as a growing collection of common data types

[1]: https://pandas.pydata.org/pandas-docs/stable/development/extending.html#extension-types