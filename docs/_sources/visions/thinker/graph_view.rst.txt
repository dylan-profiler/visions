Graph View
==========

This section discusses viewing the concepts of `visions` as graph.
We find this view intuitive to create understanding of:

- how types relate
- how operations on types are performed

It is limited for:

- intuitive understanding of membership constraints (see the nested set view).
- understanding when

The base data structure
-----------------------
The base data structure of a typeset is a directed rooted tree (graph).
Each node represents a data type.
The root note is `visions_generic`.

Each data type is associated with a set.
The root node is associated with the universal set :math:`U = \{\textrm{all data structures supported by a Series}\}`.
Each data type's set must be a proper subset of the parent's set.
Membership of a data type is defined as membership of that set.
In symbols: :math:`f: \textrm{Type} \times S \to \{True, False\}`.
There is a constraint: membership of siblings must be mutually exclusive.
This is the same as that sets for each two pairs of data types with the same parent must be disjoint, except for the missing value indicator.
For example, the `Path` and `URL` data type both have the parent data type `Object`, then in symbols: :math:`\textrm{Path} \ \{\textrm{None}\} \cap \textrm{URL} \ \{\textrm{None}\} = \emptyset`.

For the `visions_complete_set`, this base structure can be visualised as:

.. figure:: ../../../../examples/plots/typesets/typeset_complete_base.svg
   :width: 700 px
   :align: center
   :alt: Visualisation of the base data structure of the *visions_complete_set*.

   Visualisation of the base data structure of the *visions_complete_set*.

Type detection
^^^^^^^^^^^^^^

For any typeset and Pandas Series :math:`S` (i.e. a bag of values), there is the operation type detection to be :math:`f: \textrm{Typeset} \times S \to \textrm{Type}`.
The function returns the narrowest matching type given a Series.
Type detection is implemented as depth first search starting at the root note.

Relational mapping extensions
-----------------------------

We extend the data structure to support mappings from one data type to another.
Relational mappings are very similar to the edges in the base data structure.
Like the edges in the base data structure, each relational mapping is associated with a set and has to adhere to the same constraint.
In addition, it is associated with a mapping.
The domain of the mapping is the associated set.
The mapping function must be surjective.
A relational mapping may not introduce any cycles.

We can also visualise the extended structure:

.. figure:: ../../../../examples/plots/typesets/typeset_standard.svg
   :width: 700 px
   :align: center
   :alt: Visualisation of the graph structure of the *visions_standard_set*.

   Visualisation of the graph structure of the *visions_standard_set*.


.. figure:: ../../../../examples/plots/typesets/typeset_geometry.svg
   :width: 700 px
   :align: center
   :alt: Visualisation of the graph structure of the *visions_geometry_set*.

   Visualisation of the graph structure of the *visions_geometry_set*.


.. figure:: ../../../../examples/plots/typesets/typeset_complete.svg
   :width: 700 px
   :align: center
   :alt: Visualisation of the graph structure of the *visions_complete_set*.

   Visualisation of the graph structure of the *visions_complete_set*.

Type inference
^^^^^^^^^^^^^^

Type inference is type detection on the extended graph.
Similarly, we perform depth first search.
A difference is that when the type inference traverses a relational map, the values are mapped before continuing the search.

Type casting
^^^^^^^^^^^^

Type casting returns the (possibly mapped) values of type inference.
