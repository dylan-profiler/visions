import os


def path_summary(series):
    summary = {
        "common_prefix": (os.path.commonprefix(list(series)) or "No common prefix"),
        "stem_counts": series.map(lambda x: x.stem).value_counts().to_dict(),
        "suffix_counts": (series.map(lambda x: x.suffix).value_counts().to_dict()),
        "name_counts": series.map(lambda x: x.name).value_counts().to_dict(),
        "parent_counts": (series.map(lambda x: x.parent).value_counts().to_dict()),
    }

    # On add drive, root, anchor?
    return summary
