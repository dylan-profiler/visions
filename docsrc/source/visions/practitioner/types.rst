Types
*****

Types are the fundamental building block of visions, representing "logical" abstractions
of a sequence. This logical abstraction is distinct is often distinct from the
underlying in-memory implementation.

To make this distinction more concrete we can imagine the sequence `['Apple', 'Orange', 'Pear']`.

At a logical level these are of the type `Fruit` while under the hood each element is physically represented as `String`.

Types have two basic capabilities:

1. Type membership testing
2. Type relations


Membership
==========

Type membership is an important component of every visions type, membership checks answer the question `is my sequence of a type?`
In practice this looks like

.. code-block:: python

    >>> test_series in visions_string
    True

    >>> test_series in visions_integer
    False

.. seealso:: :doc:`Membership example <examples/membership>`


Relations
=========

Types also have special knowledge about their relations with other types. A relation
represents a mapping between types. Let's take the example of an integer

.. code-block:: python

    >>> from visions import visions_integer
    >>> visions_integer.get_relations()
    [IdentityRelation(visions_generic -> visions_integer),
     InferenceRelation(visions_float -> visions_integer),
     InferenceRelation(visions_string -> visions_integer)]

As we can see, there are three relations defined on the integer type. Each represents
a mapping from another type to integer. This characteristic is generally true for all
visions types; given two types, A, and B, relations defined on B represent mappings from
A to B.

By defining relations in this way types are effectively decoupled from each other.

.. seealso:: :doc:`Type Relations <relations>`
