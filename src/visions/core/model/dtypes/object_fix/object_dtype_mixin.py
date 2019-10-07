import operator
import sys

import numpy as np

from pandas.core.arrays import ExtensionArray


class ObjectArrayMixin(ExtensionArray):
    @property
    def dtype(self):
        """The dtype for this extension array"""
        return self._dtype

    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        return cls(scalars, dtype=dtype)

    @classmethod
    def _from_factorized(cls, values, original):
        return cls(values)

    @property
    def shape(self):
        """The shape of the 1D array"""
        return (len(self.data),)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, *args):
        result = operator.getitem(self.data, *args)
        if isinstance(result, tuple):
            return self._box_scalar(result)
        elif result.ndim == 0:
            return self._box_scalar(result.item())
        else:
            return type(self)(result)

    def setitem(self, indexer, value):
        """Set the 'value' inplace.
        """
        # I think having a separate than __setitem__ is good
        # since we have to return here, but __setitem__ doesn't.
        self[indexer] = value
        return self

    @property
    def nbytes(self):
        # return sys.getsizeof(self)
        # TODO: check https://stackoverflow.com/questions/11784329/python-memory-usage-of-numpy-arrays
        # TODO: add overhead of this class
        return self.data.nbytes

    def _formatting_values(self):
        return np.array(self._format_values(), dtype="object")

    def copy(self, deep=False):
        return type(self)(self.data.copy())

    @classmethod
    def _concat_same_type(cls, to_concat):
        return cls(np.concatenate([array.data for array in to_concat]))

    def tolist(self):
        return self.data.tolist()

    def argsort(self, axis=-1, kind="quicksort", order=None):
        return self.data.argsort()

    def unique(self):
        # type: () -> ExtensionArray
        # https://github.com/pandas-dev/pandas/pull/19869
        _, indices = np.unique(self.data, return_index=True)
        data = self.data.take(np.sort(indices))
        return self._from_ndarray(data)

    @classmethod
    def _from_ndarray(cls, data, copy=False):
        """Zero-copy construction of an UrlArray from an ndarray.
        Parameters
        ----------
        data : ndarray
            This should have IPType._record_type dtype
        copy : bool, default False
            Whether to copy the data.
        Returns
        -------
        ExtensionArray
        """
        if copy:
            data = data.copy()
        new = cls([])
        new.data = data
        return new

    @classmethod
    def __repr__(cls):
        formatted = cls._format_values()
        return f"{cls.__class__.__name__}({repr(formatted)})"
