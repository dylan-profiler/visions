Nested set view
===============

https://en.wikipedia.org/wiki/Nested_set_model#Example
# https://www.data-to-viz.com/graph/circularpacking.html
https://pypi.org/project/circlify/
The subset view is a way of thinking about types, typesets and relations.
It builds on the graph view.

Membership
Constraints (e.g. narrowest set)


Note empty series is always generic


Root type
---------

There is one root type, `visions_generic`, of which all values :math:`V` are member.

A type :math:`T` is associated with a parent type :math:`p`, and a subset of all the parent's values :math:`V_p`.

For example, the boolean type values :math:`\{True, False, None\} \in V`

Inference: the narrowest possible type for a set of values.


.. attention::

    So cool