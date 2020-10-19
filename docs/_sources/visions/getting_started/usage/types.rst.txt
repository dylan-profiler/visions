Types
*****

Types are the fundamental building block of visions, representing "logical" abstractions
of a sequence. This logical abstraction is distinct is often distinct from the
underlying in-memory implementation.

To make this distinction more concrete we can imagine the sequence ``['Apple', 'Orange', 'Pear']``.

At a logical level these are of the type ``Fruit`` while under the hood each element is represented by the machine as ``String``.

Types have two basic capabilities:

1. Type membership testing
2. Type relations


Membership
==========

Type membership is an important component of every visions type, membership checks answer the question "is my sequence of a type?"
In practice this looks like

.. code-block:: python

    >>> import visions as v
    >>> test_series = pd.Series(['Apple', 'Orange', 'Pear'])
    >>> test_series in v.String
    True

    >>> test_series in v.Integer
    False

.. seealso:: :doc:`Membership example <../examples/membership>`


Relations
=========

Types also have special knowledge about their relations with other types. A relation
represents a mapping between types. Let's take the example of an integer

.. code-block:: python

    >>> import visions as v
    >>> v.Integer.relations
    [IdentityRelation(Generic -> Integer),
     InferenceRelation(Float -> Integer),
     InferenceRelation(String -> Integer)]

As we can see, there are three relations defined on the integer type. Each represents
a mapping from another type to integer. This characteristic is generally true for all
visions types; given two types, A, and B, relations defined on B represent mappings from
A to B.

By defining relations in this way types are effectively decoupled from each other.

.. seealso:: :doc:`Type Relations <relations>`
