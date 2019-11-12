Nested set view
===============

This section discusses viewing the concepts of `visions` as `nested sets <https://en.wikipedia.org/wiki/Hereditarily_finite_set>`_.
We find this view intuitive to create understanding of:

- where the constraints in the graph view come from

It is limited in:

- visualising larger typesets and relational mappings (see the graph view).

The nested set structure
------------------------

The subset view is a way of thinking about types, typesets and relations and builds on the graph view.

Membership: plot set of values over the nested plot, take narrowest set that contains all values.
Constraints (e.g. narrowest set)

Note: an empty series is always generic. (e.g. corresponds to everyplace in the graph)

Root type
---------

There is one root type, `visions_generic`, of which all values :math:`V` are member.

A type :math:`T` is associated with a parent type :math:`p`, and a subset of all the parent's values :math:`V_p`.

For example, the boolean type values :math:`\{True, False, None\} \in V`

Inference: the narrowest possible type for a set of values.

Complete Set
------------

.. raw:: html
    :file: ../../../../src/visions/visualisation/circular_packing.html


.. raw:: html

    <p class="caption">
        <span class="caption-text"><a href="https://bl.ocks.org/fdlk/076469462d00ba39960f854df9acda56">Circular packing</a> of the <em>visions_complete_set</em>.</span>
        <a class="headerlink" href="#id1" title="Permalink to this image">
        </a>
    </p>
