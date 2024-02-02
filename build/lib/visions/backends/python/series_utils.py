import functools
from typing import Callable, Sequence


def sequence_not_empty(fn: Callable[..., bool]) -> Callable[..., bool]:
    """Decorator to exclude empty series"""

    @functools.wraps(fn)
    def inner(sequence: Sequence, *args, **kwargs) -> bool:
        if not any(True for _ in sequence):
            return False

        return fn(sequence, *args, **kwargs)

    return inner


def sequence_handle_none(fn: Callable[..., bool]) -> Callable[..., bool]:
    """Decorator for nullable series"""

    @functools.wraps(fn)
    def inner(sequence: Sequence, *args, **kwargs) -> bool:
        sequence = tuple(filter(None, sequence))
        return fn(sequence, *args, **kwargs)

    return inner
