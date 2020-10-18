Nested set view
===============

Sets are an excellent way to reason about types, as the definition of a type is literally constraining the possible values the data can have. We find this view intuitive to create understanding of where the the exclusivity constraint in membership relation comes from, but it is limited in understanding relational mappings (see the graph view).

Below we see a `circle packing <https://en.wikipedia.org/wiki/Circle_packing>`_ representation of the data types in the complete set.
Each circle represents the subset of all possible values that is denoted as that type.
For example, the boolean type has the possible values :math:`\{True, False, None\}`.
There is one root type, ``Generic``, of which represents all possible values.

When we perform type inference of a set of values, we find the narrowest circle that contains all values.
For example, a set :math:`\{'2020-01-01', '2020-02-02'\}` is a member of ``Generic``, ``DateTime`` and ``Date``.
``Date`` is the narrowest circle, hence the type.
Similarly, the membership relation is true when the circle includes all values.



.. raw:: html
    :file: ../../../../src/visions/visualisation/circular_packing.html


.. raw:: html

    <p class="caption">
        <span class="caption-text"><a href="https://bl.ocks.org/fdlk/076469462d00ba39960f854df9acda56">Circle packing</a> of the <em>CompleteSet</em>.</span>
        <a class="headerlink" href="#id1" title="Permalink to this image">
        </a>
    </p>
