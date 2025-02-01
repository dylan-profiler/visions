<div align="center">
  <img src="images/visions.png" width="600px"><br>
  <i>And these visions of data types, they kept us up past the dawn.</i> 
</div>


<p align="center">
  <a href="https://pypi.org/project/visions/">
    <img src="https://pepy.tech/badge/visions" />
  </a>
  <a href="https://pypi.org/project/visions/">
    <img src="https://pepy.tech/badge/visions/month" />
  </a>
  <a href="https://pypi.org/project/visions/">
    <img src="https://img.shields.io/pypi/pyversions/visions" />
  </a>
  <a href="https://pypi.org/project/visions/">
    <img src="https://badge.fury.io/py/visions.svg" />
  </a>
  <a href="https://doi.org/10.21105/joss.02145">
    <img src="https://joss.theoj.org/papers/10.21105/joss.02145/status.svg" />
  </a>
  <a href="https://mybinder.org/v2/gh/dylan-profiler/visions/master">
    <img src="https://mybinder.org/badge_logo.svg" />
  </a>
</p>

# The Semantic Data Library

``Visions`` provides a set of tools for defining and using *semantic* data types.

- [x] [Semantic type](https://dylan-profiler.github.io/visions/visions/getting_started/concepts.html#types) detection &
  inference on sequence data.

- [x] Automated data processing

- [x] Completely customizable. `Visions` makes it easy to build and modify semantic data types for domain specific
  purposes

- [x] Out of the box support for
  multiple [backend implementations](https://github.com/dylan-profiler/visions#supported-frameworks) including pandas,
  spark, numpy, and python

- [x] A robust set
  of [default types and typesets](https://dylan-profiler.github.io/visions/visions/getting_started/usage/defaults.html)
  covering the most common use cases.

Check out the complete
documentation [here](https://dylan-profiler.github.io/visions/visions/getting_started/introduction.html).

## Installation

Source code is available on [github](https://github.com/dylan-profiler/visions) and binary installers via pip.

```
# Pip
pip install visions
```

Complete installation instructions (including extras) are available in
the [docs](https://dylan-profiler.github.io/visions/visions/getting_started/installation.html).

## Quick Start Guide

If you want to play immediately check out the examples folder
on [![](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dylan-profiler/visions/master). Otherwise,
let's get some data

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
df.head(2)
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
      <th>Embarked</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>Braund, Mr. Owen Harris</td>
      <td>male</td>
      <td>22.0</td>
      <td>1</td>
      <td>0</td>
      <td>A/5 21171</td>
      <td>7.2500</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>Cumings, Mrs. John Bradley (Florence Briggs Thayer)</td>
      <td>female</td>
      <td>38.0</td>
      <td>1</td>
      <td>0</td>
      <td>PC 17599</td>
      <td>71.2833</td>
      <td>C85</td>
      <td>C</td>
    </tr>
  </tbody>
</table>


The most important abstraction in `visions` are Types - these represent semantic notions about data. You have access to
a range of well tested types like `Integer`, `Float`, and `Files` covering the most common software development use
cases.
Types can be bundled together into typesets. Behind the scenes, `visions` builds a traversable graph for any collection
of types.

```python
from visions import types, typesets

# StandardSet is the basic builtin typeset
typeset = typesets.CompleteSet()
typeset.plot_graph()
```

![](https://dylan-profiler.github.io/visions/_images/typeset_complete_base.svg)
Note: Plots require pygraphviz to be [installed](https://pygraphviz.github.io/documentation/stable/install.html).

Because of the special relationship between types these graphs can be used to detect the type of your data or _infer_ a
more appropriate one.

```python
# Detection looks like this
typeset.detect_type(df)

# While inference looks like this
typeset.infer_type(df)

# Inference works well even if we monkey with the data, say by converting everything to strings
typeset.infer_type(df.astype(str))
>> {
    'PassengerId': Integer,
    'Survived': Integer,
    'Pclass': Integer,
    'Name': String,
    'Sex': String,
    'Age': Float,
    'SibSp': Integer,
    'Parch': Integer,
    'Ticket': String,
    'Fare': Float,
    'Cabin': String,
    'Embarked': String
}
```

`Visions` solves many of the most common problems working with tabular data for example, sequences of Integers are still
recognized as integers whether they have trailing decimal 0's from being cast to float, missing values, or something
else altogether. Much of this cleaning is performed automatically providing nicely cleaned and processed data as well.

```python
cleaned_df = typeset.cast_to_inferred(df)
```

This is only a small taste of everything visions can do
including [building your own](https://dylan-profiler.github.io/visions/visions/getting_started/extending.html) domain
specific types and typesets so please check out the [API](https://dylan-profiler.github.io/visions/visions/api.html)
documentation or the [examples/](https://github.com/dylan-profiler/visions/tree/develop/examples) directory for more
info!

## Supported frameworks

Thanks to its dispatch based implementation `Visions` is able to exploit framework specific capabilities offered by
libraries like pandas and spark. Currently it works with the following backends by default.

- [Pandas](https://github.com/pandas-dev/pandas) (feature complete)
- [Numpy](https://github.com/numpy/numpy) (boolean, complex, date time, float, integer, string, time deltas, string,
  objects)
- [Spark](https://github.com/apache/spark) (boolean, categorical, date, date time, float, integer, numeric, object,
  string)
- [Python](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range) (string, float, integer,
  date time, time delta, boolean, categorical, object, complex - other datatypes are untested)

If you're using pandas it will also take advantage of parallelization tools like
[swifter](https://github.com/jmcarpenter2/swifter) if available.

It also offers a simple annotation based API for registering new implementations as needed. For example, if you wished
to extend the categorical data type to include a Dask specific implementation you might do something like

```python
from visions.types.categorical import Categorical
from pandas.api import types as pdt
import dask


@Categorical.contains_op.register
def categorical_contains(series: dask.dataframe.Series, state: dict) -> bool:
    return pdt.is_categorical_dtype(series.dtype)
```

## Contributing and support

Contributions to `visions` are welcome. For more information, please visit the community
contributions [page](https://dylan-profiler.github.io/visions/visions/contributing/contributing.html) and join on us
on [slack](https://join.slack.com/t/dylan-profiling/shared_invite/zt-11c9blvpt-AqxXD5AMS9Q6CO7UUm~cRw). The
github [issues tracker](https://github.com/dylan-profiler/visions/issues/new/choose) is used for reporting bugs, feature
requests and support questions.

Also, please check out some of the other companies and packages using `visions` including:

* [pandas profiling](https://github.com/pandas-profiling/pandas-profiling)
* [Compress*io*](https://github.com/dylan-profiler/compressio)
* [Bitrook](https://www.bitrook.com/)

If you're currently using `visions` or would like to be featured here please let us know.

## Acknowledgements

This package is part of the [dylan-profiler](https://github.com/dylan-profiler)  project. The package is core component
of [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling). More information can be
found [here](https://dylan-profiler.github.io/visions/visions/background/about.html>). This work was partially supported
by [SIDN Fonds](https://www.sidnfonds.nl/projecten/dylan-data-analysis-leveraging-automatisation).

![](https://github.com/dylan-profiler/visions/raw/master/images/SIDNfonds.png)
