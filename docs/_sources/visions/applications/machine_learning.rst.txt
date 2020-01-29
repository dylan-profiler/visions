Machine Learning
================

Detecting the Machine Learning problem type: (Multi/Single label/Class) Classification, Regression, Clustering
For example, AutoML, which is concerned with Automatic machine learning, want to perform different computations for different problem types, such as regression and classification.
The logic required for making this distinction soon grows complex and stale.
In this and related applications, there is always ambiguity: does an integer with 30 distinct values represent a categorical (classification) or count (regression problem)? There is no single answer to this question, it depends on the semantics of the data.

This is implemented in the `model-profiler <https://github.com/dylan-profiler/model-profiler>`_ (to be released).

- Probability vs Score: Another application: in machine learning we have scores and probabilities associated with predictions. As you know, a probability has nicer properties (if there are two classes, and the probability is 0.7, then 70% of the samples should actually be true). There are quite some users that confuse the two. I was thinking, wouldn't it be cool to add a subtype of Real: probability

- Encoding of categorical etc. label encoding, one-hot / dummification, random projection, embedding
  In predictive analytics and machine learning, variables are processed and encoded differently.
  The default typesets in `visions` are an useful abstraction to base the encoding and preprocessing steps on.
  For example categorical values are one-hot or `dummy coded <https://en.wikipedia.org/wiki/Categorical_variable#Dummy_coding>`_, while ordinals can be `encoded as integer <https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html#sklearn.preprocessing.OrdinalEncoder>`_.
