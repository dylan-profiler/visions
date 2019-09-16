Summaries example
=================

The following example demonstrates the summary of several `tenzing_string` types.

.. code-block:: python
    :caption: summaries_example.py
    :name: summaries_example

    from tenzing.core.model.typesets import tenzing_complete_set

    import pandas as pd

    if __name__ == "__main__":
        df = pd.DataFrame(
            {
                "latin": ["orange", "apple", "pear"],
                "cyrillic": ["Кириллица", "гласность", "демократија"],
                "mixed": ["Кириллица", "soep", "демократија"],
                "burmese": ["ရေကြီးခြင်း", "စက်သင်ယူမှု", "ဉာဏ်ရည်တု"],
                "digits": ["01234", "121223", "123123"],
                "specials": ["$", "%^&*(", "!!!~``"],
                "whitespace": ["\t", "\n", " "],
            }
        )

        ts = tenzing_complete_set()
        _ = ts.prep(df)

        summary = ts.summary_report(df)
        for key, variable_summary in summary["columns"].items():
            print(f"series with name {key} contains the unicode values {variable_summary['unicode_scripts']}")


Which prints:

.. code-block:: text

    series with name latin contains the unicode values {('Latin', 'L')}
    series with name cyrillic contains the unicode values {('Cyrillic', 'L')}
    series with name mixed contains the unicode values {('Cyrillic', 'L'), ('Latin', 'L')}
    series with name burmese contains the unicode values {('Myanmar', 'Mn'), ('Myanmar', 'Lo'), ('Myanmar', 'Mc')}
    series with name digits contains the unicode values {('Common', 'Nd')}
    series with name specials contains the unicode values {('Common', 'Sc'), ('Common', 'Sm'), ('Common', 'Po'), ('Common', 'Sk'), ('Common', 'Ps')}
    series with name whitespace contains the unicode values {('Common', 'Zs'), ('Common', 'Cc')}
