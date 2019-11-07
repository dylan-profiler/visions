Visions
=======

.. image:: images/johanna.png
   :width: 200 px
   :align: left
   :alt: Jeanne D'Arc, Image in the public domain


..


    *And these visions of data types, they kept us up past the dawn.*

    -- An Avantgardistic Data Scientist


.. Why do we need a type system?
   Python, Pandas and Numpy offer types that we can use to work with data.
   These data types
   Problem: there is no one-to-one map between types in Python, Numpy and Pandas.

Purpose of this package
-----------------------
The data models in Python, Numpy and Pandas have different ways of representing the same data, and this is problematic for data analysis.
Visions unifies the data model of Python, Numpy and Pandas, with a focus on data analysis.
For example, this package provides support for nullable booleans.

Having an unified data model, does not mean that real-world data is in that format.
The type system in this package provides a mechanism to clean this data.
For example, booleans may be stored as "Yes"/"No".
Converting these values makes the data easier to analyse and more compact in memory.

The data models are not complete enough for analysis.
Visions offers extendable support for additional types as Urls, Paths and Images.

What can it do?
---------------
Visions provides an extensible functionality to support common data analysis operations primarily

* typing common data types
* type inference on unknown data
* type conversion on real-world data
* automated data summarization

How to navigate
---------------

This documentation is divided with the following audiences in mind (you can decide which one you are at any moment):

**The New kid on the block**
    The minimal information you need to setup and start

    :doc:`Read more <getting_started/installation>`

**The Practitioner**
    Providing essential information to use type and typeset features quickly with plenty of code examples

    :doc:`Read more <practitioner/>`

**The Thinker**
    Providing a deeper understanding of concepts behind `visions`

    :doc:`Read more <thinker/>`

**The Creator**
    Providing ways to extend for your use case or contribute to the community

    :doc:`Read more <creator/>`
