def values_are_consecutive(l) -> bool:
    return sorted(l) == list(range(min(l), max(l) + 1))
