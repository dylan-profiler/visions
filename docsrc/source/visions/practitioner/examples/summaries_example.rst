Summaries example
=================

The following example demonstrates the summary of several `visions_string` types.

.. literalinclude:: ../../../../../notebooks/examples/summarize_strings.py
    :language: python
    :caption: summaries_example.py
    :name: summaries_example

Which prints:

.. code-block:: text

    Scripts in 'latin' column: {'Latin'}
    Scripts in 'cyrillic' column: {'Cyrillic'}
    Scripts in 'mixed' column: {'Latin', 'Cyrillic'}
    Scripts in 'burmese' column: {'Myanmar'}
    Scripts in 'specials' column: {'Common'}
    Scripts in 'whitespace' column: {'Common'}
    Scripts in 'jiddisch' column: {'Hebrew', 'Common'}
    Scripts in 'arabic' column: {'Arabic', 'Common'}
    Scripts in 'playing_cards' column: {'Common'}
