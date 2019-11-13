Creator
*******

One of the goals of this package is that is easy extendable for your different problems under other constraints than the defaults.
Extensions can be specific to your use case, or general for the community.

There are myriad ways to extend:

- Create a new data type (example: `email_address`)
- Create a new type set
- Create a new dtype / storage type for an existing type (reference: `cyberpandas <https://github.com/ContinuumIO/cyberpandas>`_)
- Create relations between data types (a field with the strings "J" and "N", might be Dutch or German representations of a boolean)

This section documents basic steps for contributing (e.g. testing and linting) and specific instructions on how to create each of the steps above.


.. toctree::
    :maxdepth: 1
    :hidden:

    creator/extending
    creator/contributing

