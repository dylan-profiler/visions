from tenzing.core.model_implementations.typesets import tenzing_complete_set

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
        print(variable_summary["unicode_scripts"])
