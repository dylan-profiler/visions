import collections
from urllib.parse import urlparse
import numpy as np

from tenzing.core.model.dtypes.object_dtype_mixin import ObjectArrayMixin
from tenzing.core.model.dtypes.url_dtype import UrlType


def _to_ip_array(values):
    if (isinstance(values, np.ndarray) and
            values.ndim == 1 and
            np.issubdtype(values.dtype, np.integer)):
        # We assume we're given the low bits here.
        values = values.astype("u8")
        values = np.asarray(values, dtype=UrlType._record_type)
        values['hi'] = 0

    elif not (isinstance(values, np.ndarray) and
              values.dtype == UrlType._record_type):
        # values = _to_int_pairs(values)
        pass
    return np.atleast_1d(np.asarray(values, dtype=UrlType._record_type))


class UrlArray(ObjectArrayMixin):
    """Holder for IP Addresses.
    UrlArray is a container for IPv4 or IPv6 addresses. It satisfies pandas'
    extension array interface, and so can be stored inside
    :class:`pandas.Series` and :class:`pandas.DataFrame`.
    See :ref:`usage` for more.
    """
    # A note on the internal data layout. IPv6 addresses require 128 bits,
    # which is more than a uint64 can store. So we use a NumPy structured array
    # with two fields, 'hi', 'lo' to store the data. Each field is a uint64.
    # The 'hi' field contains upper 64 bits. The think this is correct since
    # all IP traffic is big-endian.
    __array_priority__ = 1000
    _dtype = UrlType()
    _itemsize = 16
    ndim = 1
    can_hold_na = True

    def __init__(self, values, dtype=None, copy=False):
        values = _to_ip_array(values)  # TODO: avoid potential copy
        # TODO: dtype?
        if copy:
            values = values.copy()
        self.data = values

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------
    @property
    def na_value(self):
        """The missing value sentinal for IP Addresses.
        The address ``'0.0.0.0'`` is used.
        Examples
        --------
        >>> UrlArray([]).na_value
        IPv4Address('0.0.0.0')
        """
        return self.dtype.na_value

    # -------------------------------------------------------------------------
    # Interfaces
    # -------------------------------------------------------------------------

    def __repr__(self):
        formatted = self._format_values()
        return "UrlArray({!r})".format(formatted)

    @property
    def _parser(self):
        return urlparse

    def __setitem__(self, key, value):
        value = urlparse(value).data
        self.data[key] = value

    # def __iter__(self):
    #     return iter(self.to_pyipaddress())

    def astype(self, dtype, copy=True):
        from tenzing.core.model.dtypes.url_dtype import UrlType
        if isinstance(dtype, UrlType):
            if copy:
                self = self.copy()
            return self
        return super(UrlArray, self).astype(dtype)

    # ------------------------------------------------------------------------
    # Ops
    # ------------------------------------------------------------------------

    def __eq__(self, other):
        # TDOO: scalar ipaddress
        if not isinstance(other, UrlArray):
            return NotImplemented
        mask = self.isna() | other.isna()
        result = self.data == other.data
        result[mask] = False
        return result

    def __lt__(self, other):
        # TDOO: scalar ipaddress
        if not isinstance(other, UrlArray):
            return NotImplemented
        mask = self.isna() | other.isna()
        result = ((self.data['hi'] <= other.data['hi']) &
                  (self.data['lo'] < other.data['lo']))
        result[mask] = False
        return result

    def __le__(self, other):
        if not isinstance(other, UrlArray):
            return NotImplemented
        mask = self.isna() | other.isna()
        result = ((self.data['hi'] <= other.data['hi']) &
                  (self.data['lo'] <= other.data['lo']))
        result[mask] = False
        return result

    def __gt__(self, other):
        if not isinstance(other, UrlArray):
            return NotImplemented
        return other < self

    def __ge__(self, other):
        if not isinstance(other, UrlArray):
            return NotImplemented
        return other <= self

    def equals(self, other):
        if not isinstance(other, UrlArray):
            raise TypeError("Cannot compare 'UrlArray' "
                            "to type '{}'".format(type(other)))
        # TODO: missing
        return (self.data == other.data).all()

    def _values_for_factorize(self):
        return self.astype(object), np.nan

    def isna(self):
        """Indicator for whether each element is missing.
        The IPAddress 0 is used to indecate missing values.
        Examples
        --------
        >>> UrlArray(['0.0.0.0', '192.168.1.1']).isna()
        array([ True, False])
        """
        ips = self.data
        return (ips['lo'] == 0) & (ips['hi'] == 0)

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
        box = (isinstance(other, str) or
               not isinstance(other, (UrlArray, collections.Sequence)))
        if box:
            other = [other]

        addresses = other

        # Flatten all the addresses
        addresses = UrlArray(addresses)  # TODO: think about copy=False

        from pandas.core.algorithms import isin
        # TODO(factorize): replace this
        mask = isin(self, addresses)
        return mask
