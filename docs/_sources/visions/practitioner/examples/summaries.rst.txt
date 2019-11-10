Summaries example
=================

The following example demonstrates the summary of several `visions_string` types.

.. literalinclude:: ../../../../../notebooks/examples/summarize_strings.py
    :language: python
    :caption: summaries_example.py
    :name: summaries_example

Which prints:

.. code-block:: text

    | Column         | Scripts          | Categories                                                                          | Blocks                   |
    -----------------+------------------+-------------------------------------------------------------------------------------+--------------------------+
    | latin          | Latin            | Lowercase_Letter                                                                    | Basic Latin              |
    | cyrillic       | Cyrillic         | Lowercase_Letter, Uppercase_Letter                                                  | Cyrillic                 |
    | mixed          | Latin, Cyrillic  | Lowercase_Letter, Uppercase_Letter                                                  | Basic Latin, Cyrillic    |
    | burmese        | Myanmar          | Nonspacing_Mark, Spacing_Mark, Other_Letter                                         | Myanmar                  |
    | digits         | Common           | Decimal_Number                                                                      | Basic Latin              |
    | specials       | Common           | Modifier_Symbol, Currency_Symbol, Math_Symbol, Other_Punctuation, Open_Punctuation  | Basic Latin              |
    | whitespace     | Common           | Space_Separator, Control                                                            | Basic Latin              |
    | jiddisch       | Hebrew, Common   | Space_Separator, Nonspacing_Mark, Other_Letter, Decimal_Number                      | Basic Latin, Hebrew      |
    | arabic         | Arabic, Common   | Space_Separator, Other_Letter                                                       | Basic Latin, Arabic      |
    | playing_cards  | Common           | Other_Symbol                                                                        | Playing Cards            |
