from datetime import datetime

import pandas as pd


def file_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """

    stats = series.map(lambda x: x.stat())

    def convert_datetime(x):
        return datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S")

    summary = {
        "file_size": stats.map(lambda x: x.st_size),
        "file_created_time": stats.map(lambda x: x.st_ctime).map(convert_datetime),
        "file_accessed_time": stats.map(lambda x: x.st_atime).map(convert_datetime),
        "file_modified_time": stats.map(lambda x: x.st_mtime).map(convert_datetime),
    }
    return summary


def file_hash_summary(series: pd.Series, hash_algorithm="md5") -> dict:
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
        except OSError:
            raise

    summary = {
        f"hashes_{hash_algorithm}": series.map(lambda x: hash_file(x, hash_algorithm))
    }
    return summary
