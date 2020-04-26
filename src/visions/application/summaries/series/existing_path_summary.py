import pandas as pd


def existing_path_summary(series: pd.Series) -> dict:
    """Summarize file sizes

    Args:
        series: series to summarize

    Returns:
        Summary dict
    """
    summary = {"file_sizes": series.map(lambda x: x.stat().st_size)}
    return summary


def existing_path_hash_summary(series: pd.Series, hash_algorithm="md5") -> dict:
    """Include hash to summary

    Args:
        series: series to summarize
        hash_algorithm: algorithm hashlib uses to calculate the hash

    Returns:
        Summary dict
    """

    import hashlib

    def hash_file(file_name, hash_algorithm):
        hash = hashlib.new(hash_algorithm)
        chunk_size = 64000
        try:
            with open(file_name, "rb") as file:
                file_buffer = file.read(chunk_size)
                while file_buffer:
                    hash.update(file_buffer)
                    file_buffer = file.read(chunk_size)
                return hash.hexdigest()
        except IOError:
            raise

    summary = {
        "hashes_{}".format(hash_algorithm): series.map(
            lambda x: hash_file(x, hash_algorithm)
        )
    }
    return summary
