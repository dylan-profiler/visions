import collections
from urllib.parse import urlparse, ParseResult

import pandas as pd
import numpy as np
from pandas.core.arrays import IntegerArray, PandasArray
from pandas.core.dtypes.base import ExtensionDtype

# https://github.com/ContinuumIO/cyberpandas

import operator

import numpy as np

from pandas.core.arrays import ExtensionArray


class NumPyBackedExtensionArrayMixin(ExtensionArray):
    @property
    def dtype(self):
        """The dtype for this extension array, IPType"""
        return self._dtype

    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        return cls(scalars, dtype=dtype)

    @classmethod
    def _from_factorized(cls, values, original):
        return cls(values)

    @property
    def shape(self):
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
        return self._itemsize * len(self)

    def _formatting_values(self):
        return np.array(self._format_values(), dtype='object')

    def copy(self, deep=False):
        return type(self)(self.data.copy())

    @classmethod
    def _concat_same_type(cls, to_concat):
        return cls(np.concatenate([array.data for array in to_concat]))

    def tolist(self):
        return self.data.tolist()

    def argsort(self, axis=-1, kind='quicksort', order=None):
        return self.data.argsort()

    def unique(self):
        # type: () -> ExtensionArray
        # https://github.com/pandas-dev/pandas/pull/19869
        _, indices = np.unique(self.data, return_index=True)
        data = self.data.take(np.sort(indices))
        return self._from_ndarray(data)


@pd.api.extensions.register_extension_dtype
class Url(ExtensionDtype):
    name = 'Url'
    type = ParseResult
    kind = 'O'
    _record_type = np.dtype(np.object)
    na_value = np.nan

    @classmethod
    def construct_from_string(cls, string):
        if string == cls.name:
            return cls()
        else:
            raise TypeError("Cannot construct a '{}' from "
                            "'{}'".format(cls, string))

    @classmethod
    def construct_array_type(cls):
        return UrlArray


def _to_ip_array(values):
    if (isinstance(values, np.ndarray) and
            values.ndim == 1 and
            np.issubdtype(values.dtype, np.integer)):
        # We assume we're given the low bits here.
        values = values.astype("u8")
        values = np.asarray(values, dtype=Url._record_type)
        values['hi'] = 0

    elif not (isinstance(values, np.ndarray) and
              values.dtype == Url._record_type):
        # values = _to_int_pairs(values)
        pass
    return np.atleast_1d(np.asarray(values, dtype=Url._record_type))


class UrlArray(NumPyBackedExtensionArrayMixin):
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
    _dtype = Url()
    _itemsize = 16
    ndim = 1
    can_hold_na = True

    def __init__(self, values, dtype=None, copy=False):
        values = _to_ip_array(values)  # TODO: avoid potential copy
        # TODO: dtype?
        if copy:
            values = values.copy()
        self.data = values

    # @classmethod
    # def from_pyints(cls, values):
    #     """Construct an UrlArray from a sequence of Python integers.
    #     This can be useful for representing IPv6 addresses, which may
    #     be larger than 2**64.
    #     Parameters
    #     ----------
    #     values : Sequence
    #         Sequence of Python integers.
    #     Examples
    #     --------
    #     >>> UrlArray.from_pyints([0, 10, 2 ** 64 + 1])
    #     UrlArray(['0.0.0.1', '0.0.0.2', '0.0.0.3', '0:0:0:1::'])
    #     """
    #     return cls(_to_ipaddress_pyint(values))

    @classmethod
    def from_bytes(cls, bytestring):
        r"""Create an UrlArray from a bytestring.
        Parameters
        ----------
        bytestring : bytes
            Note that bytestring is a Python 3-style string of bytes,
            not a sequences of bytes where each element represents an
            IPAddress.
        Returns
        -------
        UrlArray
        Examples
        --------
        >>> arr = UrlArray([10, 20])
        >>> buf = arr.to_bytes()
        >>> buf
        b'\x00\x00\...x00\x02'
        >>> UrlArray.from_bytes(buf)
        UrlArray(['0.0.0.10', '0.0.0.20'])
        See Also
        --------
        to_bytes
        from_pyints
        """
        data = np.frombuffer(bytestring, dtype=Url._record_type)
        return cls._from_ndarray(data)

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
        new = UrlArray([])
        new.data = data
        return new

    @property
    def _as_u8(self):
        """A 2-D view on our underlying data, for bit-level manipulation."""
        return self.data.view("<u8").reshape(-1, 1)

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

    def take(self, indices, allow_fill=False, fill_value=None):
        # Can't use pandas' take yet
        # 1. axis
        # 2. I don't know how to do the reshaping correctly.
        indices = np.asarray(indices, dtype='int')

        if allow_fill and fill_value is None:
            fill_value = unpack(pack(int(self.na_value)))
        elif allow_fill and not isinstance(fill_value, tuple):
            fill_value = unpack(pack(int(fill_value)))

        if allow_fill:
            mask = (indices == -1)
            if not len(self):
                if not (indices == -1).all():
                    msg = "Invalid take for empty array. Must be all -1."
                    raise IndexError(msg)
                else:
                    # all NA take from and empty array
                    took = (np.full((len(indices), 2), fill_value, dtype='>u8')
                              .reshape(-1).astype(self.dtype._record_type))
                    return self._from_ndarray(took)
            if (indices < -1).any():
                msg = ("Invalid value in 'indicies'. Must be all >= -1 "
                       "for 'allow_fill=True'")
                raise ValueError(msg)

        took = self.data.take(indices)
        if allow_fill:
            took[mask] = fill_value

        return self._from_ndarray(took)

    # -------------------------------------------------------------------------
    # Interfaces
    # -------------------------------------------------------------------------

    def __repr__(self):
        formatted = self._format_values()
        return "UrlArray({!r})".format(formatted)

    def _format_values(self):
        formatted = []
        # TODO: perf
        for i in range(len(self)):
            hi, lo = self.data[i]
            if lo == -1:
                formatted.append("NA")
            elif hi == 0 and lo <= _IPv4_MAX:
                formatted.append(ipaddress.IPv4Address._string_from_ip_int(
                    int(lo)))
            elif hi == 0:
                formatted.append(ipaddress.IPv6Address._string_from_ip_int(
                    int(lo)))
            else:
                # TODO:
                formatted.append(ipaddress.IPv6Address._string_from_ip_int(
                    (int(hi) << 64) + int(lo)))
        return formatted

    @staticmethod
    def _box_scalar(scalar):
        return ipaddress.ip_address(combine(*scalar))

    @property
    def _parser(self):
        from .parser import to_ipaddress
        return to_ipaddress

    def __setitem__(self, key, value):
        from .parser import to_ipaddress

        value = to_ipaddress(value).data
        self.data[key] = value

    def __iter__(self):
        return iter(self.to_pyipaddress())

    # ------------------------------------------------------------------------
    # Serializaiton / Export
    # ------------------------------------------------------------------------

    def to_pyipaddress(self):
        """Convert the array to a list of scalar IP Adress objects.
        Returns
        -------
        addresses : List
            Each element of the list will be an :class:`ipaddress.IPv4Address`
            or :class:`ipaddress.IPv6Address`, depending on the size of that
            element.
        See Also
        --------
        UrlArray.to_pyints
        Examples
        ---------
        >>> UrlArray(['192.168.1.1', '2001:db8::1000']).to_pyipaddress()
        [IPv4Address('192.168.1.1'), IPv6Address('2001:db8::1000')]
        """
        import ipaddress
        return [ipaddress.ip_address(x) for x in self._format_values()]

    def to_pyints(self):
        """Convert the array to a list of Python integers.
        Returns
        -------
        addresses : List[int]
            These will be Python integers (not NumPy), which are unbounded in
            size.
        See Also
        --------
        UrlArray.to_pyipaddresses
        UrlArray.from_pyints
        Examples
        --------
        >>> UrlArray(['192.168.1.1', '2001:db8::1000']).to_pyints()
        [3232235777, 42540766411282592856903984951653830656]
        """
        return [combine(*map(int, x)) for x in self.data]

    def to_bytes(self):
        r"""Serialize the UrlArray as a Python bytestring.
        This and :meth:UrlArray.from_bytes is the fastest way to roundtrip
        serialize and de-serialize an UrlArray.
        See Also
        --------
        UrlArray.from_bytes
        Examples
        --------
        >>> arr = UrlArray([10, 20])
        >>> arr.to_bytes()
        b'\x00\x00\...x00\x02'
        """
        return self.data.tobytes()

    def astype(self, dtype, copy=True):
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

        networks = []
        addresses = []

        # if not isinstance(other, UrlArray):
        #     for net in other:
        #         net = _as_ip_object(net)
        #         if isinstance(net, (ipaddress.IPv4Network,
        #                             ipaddress.IPv6Network)):
        #             networks.append(net)
        #         if isinstance(net, (ipaddress.IPv4Address,
        #                             ipaddress.IPv6Address)):
        #             addresses.append(ipaddress.IPv6Network(net))
        # else:
        addresses = other

        # Flatten all the addresses
        addresses = UrlArray(addresses)  # TODO: think about copy=False

        mask = np.zeros(len(self), dtype='bool')
        for network in networks:
            mask |= self._isin_network(network)

        # no... we should flatten this.
        mask |= self._isin_addresses(addresses)
        return mask

    def _isin_network(self, other):
        """Check whether an array of addresses is contained in a network."""
        # A network is bounded below by 'network_address' and
        # above by 'broadcast_address'.
        # UrlArray handles comparisons between arrays of addresses, and NumPy
        # handles broadcasting.
        net_lo = type(self)([other.network_address])
        net_hi = type(self)([other.broadcast_address])

        return (net_lo <= self) & (self <= net_hi)

    def _isin_addresses(self, other):
        """Check whether elements of self are present in other."""
        from pandas.core.algorithms import isin
        # TODO(factorize): replace this
        return isin(self, other)


s = pd.Series(['http://www.google.com', 'http://www.ru.nl'] * 100, dtype="Url")
s2 = pd.Series([urlparse('http://www.google.com'), urlparse('http://www.ru.nl')] * 100, dtype="Url")
s3 = pd.Series(['http://www.google.com', 'http://www.ru.nl'] * 100)
s4 = pd.Series([urlparse('http://www.google.com'), urlparse('http://www.ru.nl')] * 100)


print(f"{s.memory_usage(deep=True)} bytes, {s.dtype} dtype, from string")
print(f"{s2.memory_usage(deep=True)} bytes, {s2.dtype} dtype, from ParseResult")
print(f"{s3.memory_usage(deep=True)} bytes, {s3.dtype} dtype, from string")
print(f"{s4.memory_usage(deep=True)} bytes, {s4.dtype} dtype, from ParseResult")
