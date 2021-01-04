Machine Learning
================

In the field of pattern recognition and machine learning, we consider the supervised scenario where we have a labelled training set which we use to learn the parameters of a model that predicts a target vector.

Problem type inference
----------------------
We encounter the importance of semantic data types in machine learning right away, as the field distinguishes two kinds of supervised learning tasks.
When predicting a finite number of discrete categories, the task is known as classification, and when predicting one or more continuous variables, it is known as regression [bishop2006pattern]_.
Automatically distinguishing the two might be seen trivial, however, there are ambiguous cases.
Values represented by the computer as '0' and '1' could be both binary (a special case of a categorical variable) or continuous (a count).
While in theory, we could enforce categories to have a string representation and continuous values integer or float representations, this is not the case with real-world datasets.
Often data is stored in plain-text CSV files, where the distinction is lost.
Automatically distinguishing between problem type is not merely a mental exercise, it is actively used in AutoML (the process of automatically applying machine learning, not the product).

For an example, see :doc:`usage of typesets <../getting_started/examples/ml_problem_set>`.

Confidence scores
-----------------
When classification is used in practice, we often do not want to rely solely on the label prediction and want a measure of certainty that the model is correct.
This is especially the case when a decision can have an enormous impact.
Consider a medical diagnosis problem where, based on an fMRI scan, we wish to determine whether the patient has cancer.
The cost of classifying a non-cancerous scan as cancerous is not as high as vice versa.
One method of certainty is to let the model output a confidence score for each prediction, indicating the certainty with which the prediction is taken.
A reliable confidence score gives us the option to avoid automatically making decisions on difficult cases.
When we can assume that the confidence score is a probability, we can draw from tools provided by probability theory.
In this special case, the confidence has to adhere to the rules of probability, such as it should be in the interval [0, 1] and that for samples predicted with 0.8 confidence that should mean that about 80% of these samples belong to the true class.
A classifier is said to be well-calibrated when it adheres to these rules.

Models as Logistic regression return well-calibrated predictions by default, while others return biased scores, such as Random Forest or SVM classifiers.
One can perform various analysis to understand how well a classifier is calibrated.

A hierarchical type system such as ``visions`` can be used to differentiate between confidence scores and probabilities.
One then could perform specialised types of analysis based on this type.

The *scikit-learn* package provides excellent resources for model calibration [#f1]_.
For more background on the relevant aspects of probability and decision theory, we recommend reading [bishop2006pattern]_, chapter 1.5, p. 38-42.

Encoding variables
------------------
Another case in machine learning where semantic types are relevant is the encoding of variables.
There are various ways to encode variables in predictive models that depend on its statistical type.
For example, categorical values can be encoded as one-hot or `dummy coded <https://en.wikipedia.org/wiki/Categorical_variable#Dummy_coding>`_, `random projection or via learned representations <https://mlbox.readthedocs.io/en/latest/features.html#categorical-features>`_.
Ordinals can be `encoded as integer <https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html#sklearn.preprocessing.OrdinalEncoder>`_ (or embedded).
Likewise, strategies for filling missing values may also depend on the data type.

Model profiling
---------------
There are plans to implement specific model statistics in the `model-profiler <https://github.com/dylan-profiler/model-profiler>`_ package (to be released).
This package will focus on summarization of a model or sets of predictions and will be based on a custom ``visions`` typeset.
Relevant statistics encompass error metrics, analysis of residuals and model explainers.

.. [bishop2006pattern] Bishop, C. M. (2006). Pattern recognition and machine learning. springer.

.. rubric:: Footnotes

.. [#f1] https://scikit-learn.org/stable/modules/calibration.html