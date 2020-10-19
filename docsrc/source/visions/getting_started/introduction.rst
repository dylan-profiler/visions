Introduction
============

.. Tmp
   figure:: images/johanna.png
   :width: 200 px
   :align: right
   :alt: Jeanne D'Arc, Image in the public domain

..   The Maid of Orléans
      *And these visions of data types, they kept us up past the dawn.*


.. a-- An Avantgardistic Data Scientist


.. Why do we need a type system?
   Python, Pandas and Numpy offer types that we can use to work with data.
   These data types
   Problem: there is no one-to-one map between types in Python, Numpy and Pandas.

.. Why this package?
   -----------------

This package lets you work with efficient, extendable semantic data types on tabular data in Python.
The right abstraction of your data, through these types, is a powerful tool to effectively reduce complexity and increase performance, helping solve problems you are working on.
Type systems are extremely flexible and applications include dataset creation, exploratory data analysis and data cleaning.

.. The data models in Python, Numpy and Pandas have different ways of representing the same data, and this is problematic for data analysis.
   Visions unifies the data model of Python, Numpy and Pandas, with a focus on data analysis.
   For example, this package provides support for nullable booleans.

.. Having an unified data model, does not mean that real-world data is in that format.
   The type system in this package provides a mechanism to clean this data.
   For example, booleans may be stored as "Yes"/"No".
   Converting these values makes the data easier to analyse and more compact in memory.

.. The data models are not complete enough for analysis.
   Visions offers extendable support for additional types as Urls, Paths and Images.

What can it do?
---------------

You can use the package in the following way:

- You pick the types and typeset that are relevant to your problem.
  The types and typeset can be chosen from the default library, or you can create custom types.
  (application: modeling the problem)

- ``visions`` can detect types of your data.

- It lets you define mappings from one type to another.
  This is helpful when working with real-world data.
  Provided these mappings, ``visions`` can infer and convert types.
  (application: data cleaning)

- You can then develop applications using the abstraction provided by the types.

How does it do it?
------------------

Essentially, ``visions`` does the following:

- It builds on Pandas, Numpy and Python.
- It extends the data types in Pandas to solve storage and implementation issues.
- On top of that it models typesets as graphs (networkx) and provides graph traversal algorithms for type detection, inference and conversion.

..
   How to navigate
   ---------------

   This documentation is subdivided with the following audiences in mind (you can decide which one you are at any moment):

   **The New Kid On The Block**
       The basic information you need to setup and start

       :doc:`Read more <getting_started/installation>`
   **The Practitioner**
       Providing practical information to use type's and typeset's features quickly, with plenty of code examples

       :doc:`Read more <practitioner/>`
   **The Thinker**
       Providing a deeper understanding of concepts behind ``visions``

       :doc:`Read more <thinker/>`
   **The Creator**
       Providing ways to extend for your use case or contribute to the community

       :doc:`Read more <creator/>`
