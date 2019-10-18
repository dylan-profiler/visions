Summaries example
=================

The following example demonstrates the summary of several `visions_string` types.

.. literalinclude:: ../../../../../notebooks/examples/summarize_strings.py
    :language: python
    :caption: summaries_example.py
    :name: summaries_example

Which prints:

.. code-block:: text

    series with name latin contains the unicode values {('Latin', 'L')}
    series with name cyrillic contains the unicode values {('Cyrillic', 'L')}
    series with name mixed contains the unicode values {('Cyrillic', 'L'), ('Latin', 'L')}
    series with name burmese contains the unicode values {('Myanmar', 'Mn'), ('Myanmar', 'Lo'), ('Myanmar', 'Mc')}
    series with name digits contains the unicode values {('Common', 'Nd')}
    series with name specials contains the unicode values {('Common', 'Sc'), ('Common', 'Sm'), ('Common', 'Po'), ('Common', 'Sk'), ('Common', 'Ps')}
    series with name whitespace contains the unicode values {('Common', 'Zs'), ('Common', 'Cc')}
