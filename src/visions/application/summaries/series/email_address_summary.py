import pandas as pd


def email_address_summary(series: pd.Series) -> dict:
    summary = {}

    local = []
    fqdn = []
    for v in series.drop().values:
        local.append(v.local)
        fqdn.append(v.fqdn)

    summary["local_counts"] = pd.Series(local).value_counts().to_dict()
    summary["fqdn_counts"] = pd.Series(fqdn).value_counts().to_dict()

    return summary
