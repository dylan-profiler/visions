Data Summarization
==================

The process of exploratory data analysis (EDA) or data summarization intends to get a high-level overview of the main characteristics of a dataset.
This is an essential step when working with a new dataset, and therefore is worthwhile automating.

An effective summary of the dataset goes beyond the *machine* type representations of the dataset.
If a variable stores a URL as a string, we might be interested if every URL has the "https" scheme.
There is also overlap between machine types, where ``min``, ``max`` and ``range`` are sensible statistics for real values as well as dates.

A demonstration of the visions package for type summarization for demonstration purposes can be found in `pandas-profiling <https://github.com/pandas-profiling/pandas-profiling>`_, a dedicated package that provides these summarizations.
