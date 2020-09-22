import functools
from collections import OrderedDict

import pandas as pd


class LRUCacher:
    def __init__(self, hash_func, max_length, value_func):
        self.hash_func = hash_func
        self.max_length = max_length
        self.value_func = value_func
        self.cache = OrderedDict()

    def __getitem__(self, key):
        value = self.cache[key]
        self.cache.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.max_length:
            oldest = next(iter(self.cache))
            del self.cache[oldest]

    def get_key(self, *args):
        return self.hash_func(*args)

    def get(self, *args):
        id_key = self.get_key(*args)
        if id_key not in self.cache:
            self[id_key] = self.value_func(*args)
        return self[id_key]


def lru_cache(hash_func, max_length):
    def func_inner(func):
        cache = LRUCacher(hash_func, max_length, func)

        @functools.wraps(func)
        def inner(*args):
            return cache.get(*args)

        return inner

    return func_inner


def mutable_pseudo_hash(data, node, graph):
    # return id((data, node, graph))
    try:
        if isinstance(data, pd.DataFrame):
            data_hash = hash(hash(tuple(data[col])) for col in data.columns)
        else:
            data_hash = hash(tuple(data.values))
    except:
        return id((data, node, graph))

    return hash((data_hash, node, graph))
