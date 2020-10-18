Theory
******

Background
----------

``visions`` primary goal is to develop a robust mechanism for defining and using
*semantic* data types. These represent conceptual or logical notions of meaning
and is distinct from the machine representation of data on disk. For example,
we might say sequence :math:`S` is of semantic type ``probability`` when
:math:`S \in [0, 1]` or ``date`` when each element is stored on the computer as a
``datetime.datetime`` object with all time components identically ``0``.

Most data analytics libraries users are already familiar with have their own data
types builtin, usually tightly coupled with the machine representation of the data
used by the library. We wanted to give users as much flexibility to design and work
in the representations specific to their problems and domain and in order to do that
we had to give users the freedom to make their own types. This left a few key
challenges to solve.


Open Challenges
---------------

1. Finding a minimal representation of semantic types
2. Detecting the semantic type of a sequence
3. ``visions`` is interested in the semantic meaning of data and therefore should be able to infer the "intended" type of a sequence regardless of it's machine representation (e.g. the string ``'1.0'`` should be recognized as the number ``1``).


We want to do all of this while keeping types easy to use, performant, and deterministic.

Since users are free to imagine any possible type, different problem domains might
require contradictory notions of the same type. Where a data scientist might be
interested in probability as a sequence of values bounded such that :math:`x \in [0, 1]`,
a business analyst might instead be interested in a definition where  :math:`x \in [0, 100]`.


The ``visions`` Solution
------------------------

We solve all of these problems by introducing three conceptual ideas, ``visions``
types, typesets, and relations.

A *type* at minimum requires only a single validation function which takes as its
argument a sequence and tests whether the input is of its type or not, returning
boolean. It optionally can contain relationships which we will describe in a moment.

A *typeset* is a collection of types. Behind the scenes visions uses the relationships
defined on each type in the typeset to construct a relationship graph. When properly
constructed this graph can be used to deterministically detect the current semantic types
of a sequence (or dataset) or to infer a more representative type for the data.

A *relation* object is responsible for mapping sequences between ``visions`` types.
Each relation is composed of two functions, the first validates whether a
mapping can be performed without loss of precision (i.e. '1.0' can be cast to
integer while 1.1 cannot), the second is a surjective function responsible for
actually performing the mapping.

In practice, we distinguish ``relations`` into two categories as well, the first
called ``Identity Relations`` require no transformation to the underlying machine
type of the data (float(1.1) -> probability(1.1) where the second, ``Inference Relations``,
have to coerce the sequence between machine types ('1.1' -> 1.1).


Why it works
------------

We will be using the language of trees and sets to understand how this all comes together
and start by defining a semantic type as the set of all sequences with some
consistent semantic meaning. A typeset is then a directed rooted tree whose nodes
are types with the root defined as the generic type associated with the universal set.

Relations are directed edges between two nodes (types) in a relation graph (typeset).
They are also defined on types such that a relation between types ``A`` and ``B``,
``Relation(A -> B)``, would be defined as an attribute of B. In order words, they
are mappings *to* a type, not *from*.

Following this, we can construct a relation graph from *any* collection of provided
types and associated relations. We define our dual objective of type detection and
type inference as the task of determining the most unique possible type
specification available to the typeset either with coercion of machine types (inference),
or without (detection).

Both tasks are akin to simple traversal of the relation graph. In order to guarantee
all sequences map to only a single type we require the graph be *decidable*.
This is equivalent to saying sets of any two pairs of data types with the same
parent must be disjoint, except for the missing value indicator. Additionally,
relations are not permitted to introduce cycles into the tree.
