import pandas as pd
from pandas.core.dtypes.base import ExtensionDtype
from urllib.parse import ParseResult
import collections
from urllib.parse import urlparse
import numpy as np

from tenzing.core.model.dtypes.object_fix.object_dtype_mixin import ObjectArrayMixin


@pd.api.extensions.register_extension_dtype
class UrlType(ExtensionDtype):
    name = "Url"
    type = ParseResult
    kind = "O"
    _record_type = np.dtype(np.object)
    na_value = None

    @classmethod
    def construct_from_string(cls, string):
        if string == cls.name:
            return cls()
        else:
            raise TypeError("Cannot construct a '{}' from " "'{}'".format(cls, string))

    @classmethod
    def construct_array_type(cls):
        return UrlArray


class UrlArray(ObjectArrayMixin):
    """Holder for IP Addresses.
    UrlArray is a container for IPv4 or IPv6 addresses. It satisfies pandas'
    extension array interface, and so can be stored inside
    :class:`pandas.Series` and :class:`pandas.DataFrame`.
    See :ref:`usage` for more.
    """

    __array_priority__ = 1000
    _dtype = UrlType()
    ndim = 1
    can_hold_na = True

    def __init__(self, values, dtype=None, copy=False):
        if (
            isinstance(values, np.ndarray)
            and values.ndim == 1
            and np.issubdtype(values.dtype, np.unicode)
        ):
            values = np.asarray(values, dtype=UrlType._record_type)

        values = np.atleast_1d(np.asarray(values, dtype=UrlType._record_type))

        if copy:
            values = values.copy()
        self.data = values

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------
    @property
    def na_value(self):
        return self.dtype.na_value

    # -------------------------------------------------------------------------
    # Interfaces
    # -------------------------------------------------------------------------

    @property
    def _parser(self):
        return urlparse

    def __setitem__(self, key, value):
        value = urlparse(value).data
        self.data[key] = value

    def astype(self, dtype, copy=True):
        if isinstance(dtype, self._dtype):
            if copy:
                self = self.copy()
            return self
        return super().astype(dtype)

    # ------------------------------------------------------------------------
    # Ops
    # ------------------------------------------------------------------------

    def __eq__(self, other):
        if not isinstance(other, UrlArray):
            return NotImplemented
        mask = self.isna() | other.isna()
        result = self.data == other.data
        result[mask] = False
        return result

    def equals(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f"Cannot compare '{self.__class__.__name__}' to type '{type(other)}'"
            )
        return (self.data == other.data).all()

    def _values_for_factorize(self):
        return self.astype(object), np.nan

    def isna(self):
        """Indicator for whether each element is missing.
        The IPAddress 0 is used to indicate missing values.
        Examples
        --------
        >>> UrlArray(['0.0.0.0', '192.168.1.1']).isna()
        array([ True, False])
        """
        ips = self.data
        return ips.isna()

    # TODO: add isin domain
    # s.isin('domain.com')
    def isin(self, other):
        """Check whether elements of `self` are in `other`.
        Comparison is done elementwise.
        Parameters
        ----------
        other : str or sequences
            For ``str`` `other`, the argument is attempted to
            be converted to an :class:`ipaddress.IPv4Network` or
            a :class:`ipaddress.IPv6Network` or an :class:`UrlArray`.
            If all those conversions fail, a TypeError is raised.
            For a sequence of strings, the same conversion is attempted.
            You should not mix networks with addresses.
            Finally, other may be an ``UrlArray`` of addresses to compare to.
        Returns
        -------
        contained : ndarray
            A 1-D boolean ndarray with the same length as self.
        Examples
        --------
        Comparison to a single network
        >>> s = UrlArray(['192.168.1.1', '255.255.255.255'])
        >>> s.isin('192.168.1.0/24')
        array([ True, False])
        Comparison to many networks
        >>> s.isin(['192.168.1.0/24', '192.168.2.0/24'])
        array([ True, False])
        Comparison to many IP Addresses
        >>> s.isin(['192.168.1.1', '192.168.1.2', '255.255.255.1']])
        array([ True, False])
        """
        box = isinstance(other, str) or not isinstance(
            other, (UrlArray, collections.Sequence)
        )
        if box:
            other = [other]

        addresses = other

        # Flatten all the addresses
        addresses = UrlArray(addresses)  # TODO: think about copy=False

        from pandas.core.algorithms import isin

        # TODO(factorize): replace this
        mask = isin(self, addresses)
        return mask
