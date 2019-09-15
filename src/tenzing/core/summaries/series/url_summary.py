import pandas as pd


def url_summary(series):
    summary = {}

    keys = ["scheme", "netloc", "path", "query", "fragment"]
    url_parts = dict(zip(keys, zip(*series)))
    for name, part in url_parts.items():
        summary["{}_counts".format(name.lower())] = (
            pd.Series(part).value_counts().to_dict()
        )

    return summary
