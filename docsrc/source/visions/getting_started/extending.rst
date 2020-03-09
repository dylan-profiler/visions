Extending
=========

Custom Type (from scratch)
---------------------------

Each `visions` type is a subclass of  `VisionsBaseType` requiring a unique implementation of two methods:

1. `get_relations`. Returns the set of relations mapping from another type to the current type.
2. `contains_op`. Checks whether a series is of the type visions_type, returns Bool.

Let's inspect the source code for `visions_ordinal` to gather intuition.

.. code-block:: python
    :caption: visions_ordinal.py
    :name: visions_ordinal

    from visions.core.models import VisionsBaseType

    def _get_relations():
        from visions.core.implementations.types import visions_categorical

        relations = [IdentityRelation(visions_ordinal, visions_categorical)]
        return relations

    class visions_ordinal(VisionsBaseType):
        """**Ordinal** implementation of :class:`visions.core.model.type.VisionsBaseType`.
        Examples:
            >>> x = pd.Series([1, 2, 3, 1, 1], dtype='category')
            >>> x in visions_ordinal
            True
        """

        @classmethod
        def get_relations(cls):
            return _get_relations()

        @classmethod
        def contains_op(cls, series: pd.Series) -> bool:
            return pdt.is_categorical_dtype(series) and series.cat.ordered


In this example, ordinal declares a single `IdentityRelation` from categorical. The meaning
of `IdentityRelation` is not particularly important in this case, just know it means the mapping
function between categorical and ordinal is the identity function.

We can also see the `contains_op` requires the sequence to be an ordered categorical machine type representation.

Alternatively you can choose to base a type on an existing type.
This is convenient when you only change a single relation.

.. code-block:: python

    visions



.. note::

    Your custom type might be helpful for others, in which case you can choose to contribute it to `visions`.
    Read more on :doc:`how to contribute <../contributing/type>`.

Another example
---------------

The default typesets in `visions` consider `boolean` and `categorical` to be distinct types.
In fact, `boolean` is a special case of `categorical` where the number of categories is 2 and contains the values "True" and "False" ("Man" and "Woman" wouldn't be binary).

Note that for data analysis, the distinction makes sense.
For a boolean we could the true/false ratio for example.

See: `examples/data_analysis` for an example.

Custom Types (extend a type)
----------------------------

Another option is to create a new type based on an existing type.
This is useful for small changes, such as adding a single relation.

Each type has the method `extend_relations` for this purpose.

.. code-block:: python
   :caption: Add a inference relation from integer to datetime (YYYYMMDD)

    from visions.core.implementations.types.visions_integer import _get_relations, visions_integer
    from visions.lib.relations.integer_to_datetime import integer_to_datetime_year_month_day

    compose_relations = lambda: _get_relations() + [integer_to_datetime_year_month_day()]
    visions_integer_ddt = visions_integer.extend_relations('with_datetime', compose_relations)

    print(visions_integer_ddt)
    # Prints: visions_integer[with_datetime]

.. hint::

    While developing new type relations, you can use this helper function to debug:

    .. code-block:: python

       for column, type_before, type_after in compare_detect_inference_frame(df, typeset):
            print(f"{column} was {type_before} is {type_after}")


Custom Typesets (from scratch)
------------------------------

Although `visions` comes with an array of starter typesets suitable for most standard usage
you may quickly find yourself looking to expand upon those types to suit your own domain specific
needs. In order to meet those needs there are a number of easy mechanisms to either extend pre-existing
typesets or define your own from scratch.

For example, you could define a custom typeset with only time specific types as follows:

.. code-block:: python
    :caption: Custom time typeset

    class visions_custom_set(VisionTypeset):
        """Typeset that exclusively supports time related types

        Includes support for the following types:

        - visions_datetime
        - visions_timedelta
        - visions_date
        - visions_time

        """

        def __init__(self):
            types = [
                visions_datetime,
                visions_timedelta,
                visions_date,
                visions_time,
            ]
            super().__init__(types)


or even more simply,


.. code-block:: python
    :caption: Custom time typeset (simplified)

    types = [visions_datetime, visions_timedelta, visions_date, visions_time]
    visions_custom_set = VisionTypeset(types)


Custom typesets (extend typeset)
--------------------------------

Alternatively, typesets support a limited algebra allowing you to define new typesets
based on simple manipulations to pre-existing sets.

.. code-block:: python
    :caption: Custom time typeset

    typeset = visions_complete_set() - visions_time + visions_date


Just like addition and subtraction elsewhere in Python, you can split these operations up
in any way imaginable:

.. code-block:: python

    rdw_typeset = visions_complete_set()
    rdw_typeset -= visions_bool
    rdw_typeset += visions_bool_nl
    rdw_typeset -= visions_integer
    rdw_typeset += visions_integer_ddt
    rdw_typeset -= visions_categorical
    rdw_typeset += visions_categorical_str

.. seealso:: Engineer view on constraint checking
