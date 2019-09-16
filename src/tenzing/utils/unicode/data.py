from pathlib import Path


def download_file_http(url: str, dest: Path):
    import requests

    f = requests.get(url)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(f.content)


def download_file_ftp(url: str, dest: Path):
    import urllib.request

    urllib.request.urlretrieve(url, str(dest))


def get_files(file_names):
    # Alternatively:
    # url = "http://www.unicode.org/Public/UNIDATA/Scripts.txt"

    for file_name in file_names:
        url = f"ftp://ftp.unicode.org/Public/UNIDATA/{file_name}"
        dest = Path("data") / file_name
        if not dest.exists():
            download_file_ftp(url, dest)


if __name__ == "__main__":
    # https://www.unicode.org/reports/tr44/#PropList.txt
    get_files(
        [
            "Scripts.txt",
            "PropList.txt",
            "DerivedCoreProperties.txt",
            "PropertyValueAliases.txt",
            "Blocks.txt",
            "UnicodeData.txt",
            "DerivedNormalizationProps.txt",
            "ScriptExtensions.txt",
            "NameAliases.txt",
            "CaseFolding.txt",
            "BidiBrackets.txt",
            "LineBreak.txt",
            "EastAsianWidth.txt",
            "NamedSequences.txt",
        ]
    )
