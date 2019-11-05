Visions
=======

.. image:: images/johanna.png
   :width: 200 px
   :align: center
   :alt: Jeanne D'Arc, Image in the public domain


..


    And these visions of data types, they kept us up past the dawn.

    -- An Avantgardistic Data Scientist


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

This documentation is setup with the following audiences in mind (you can decide which one you are at any moment):

- The practitioner: Providing essential information to get started quickly
- The thinker: Providing a deeper understanding of concepts behind `visions`
- The creator: Providing ways to extend for your use case or contribute to the community
