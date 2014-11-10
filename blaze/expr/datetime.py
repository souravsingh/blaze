from __future__ import absolute_import, division, print_function

from .expressions import Expr, ElemWise
from datashape import dshape, Record, DataShape, Unit, Option, date_, datetime_
import datashape

__all__ = ['DateTime', 'Date', 'date', 'Year', 'year', 'Month', 'month', 'Day',
        'day', 'Hour', 'hour', 'Second', 'second', 'Millisecond',
        'millisecond', 'Microsecond', 'microsecond', 'Date', 'date', 'Time',
        'time', 'UTCFromTimestamp', 'DateTimeTruncate']

class DateTime(ElemWise):
    """ Superclass for datetime accessors """
    __slots__ = '_child',

    def __str__(self):
        return '%s.%s' % (str(self._child), type(self).__name__.lower())

    @property
    def schema(self):
        return dshape(self._dtype)

    @property
    def _name(self):
        return '%s_%s' % (self._child._name, self.attr)

    @property
    def attr(self):
        return type(self).__name__.lower()


class Date(DateTime):
    _dtype = datashape.date_

def date(expr):
    return Date(expr)

class Year(DateTime):
    _dtype = datashape.int32

def year(expr):
    return Year(expr)

class Month(DateTime):
    _dtype = datashape.int32

def month(expr):
    return Month(expr)

class Day(DateTime):
    _dtype = datashape.int32

def day(expr):
    return Day(expr)

class Time(DateTime):
    _dtype = datashape.time_

def time(expr):
    return Time(Expr)

class Hour(DateTime):
    _dtype = datashape.int32

def hour(expr):
    return Hour(expr)

class Minute(DateTime):
    _dtype = datashape.int32

def minute(expr):
    return Minute(expr)

class Second(DateTime):
    _dtype = datashape.int32

def second(expr):
    return Second(expr)

class Millisecond(DateTime):
    _dtype = datashape.int64

def millisecond(expr):
    return Millisecond(expr)

class Microsecond(DateTime):
    _dtype = datashape.int64

def microsecond(expr):
    return Microsecond(expr)

class UTCFromTimestamp(DateTime):
    _dtype = datashape.datetime_

def utcfromtimestamp(expr):
    return UTCFromTimestamp(expr)

units = ['year', 'month', 'week', 'day', 'hour', 'minute', 'second',
'millisecond', 'microsecond', 'nanosecond']


_unit_aliases = {'y': 'year', 'w': 'week', 'd': 'day', 'date': 'day',
    'h': 'hour', 's': 'second', 'ms': 'millisecond', 'us': 'microsecond',
    'ns': 'nanosecond'}

def normalize_time_unit(s):
    """ Normalize time input to one of 'year', 'second', 'millisecond', etc..

    Example
    -------

    >>> normalize_time_unit('milliseconds')
    'millisecond'
    >>> normalize_time_unit('ms')
    'millisecond'
    """
    s = s.lower().strip()
    if s in units:
        return s
    if s in _unit_aliases:
        return _unit_aliases[s]
    if s[-1] == 's':
        return normalize_time_unit(s.rstrip('s'))

    raise ValueError("Do not understand time unit %s" % s)


class DateTimeTruncate(DateTime):
    __slots__ = '_child', 'measure', 'unit'

    @property
    def _dtype(self):
        if units.index('day') >= units.index(self.unit):
            return datashape.date_
        else:
            return datashape.datetime_


def truncate(expr, *args, **kwargs):
    """ Truncate datetime expression

    Example
    -------

    >>> from blaze import Symbol, compute
    >>> from datetime import datetime
    >>> s = Symbol('s', 'datetime')

    >>> expr = s.truncate(10, 'minutes')
    >>> compute(expr, datetime(2000, 6, 25, 12, 35, 10))
    datetime.datetime(2000, 6, 25, 12, 30)

    >>> expr = s.truncate(1, 'week')
    >>> compute(expr, datetime(2000, 6, 25, 12, 35, 10))
    datetime.date(2000, 6, 19)

    Alternatively use keyword arguments to specify unit and measure

    >>> # expr = s.truncate(2, 'weeks')
    >>> expr = s.truncate(weeks=2)
    """
    if args:
        assert not kwargs
        measure, unit = args
    if kwargs:
        assert not args
        [(unit, measure)] = kwargs.items()
    return DateTimeTruncate(expr, measure, normalize_time_unit(unit))


from .expressions import schema_method_list, method_properties
from datashape.predicates import isdatelike, isnumeric

schema_method_list.extend([
    (isdatelike, set([year, month, day, hour, minute, date, time, second,
                      millisecond, microsecond, truncate])),
    (isnumeric, set([utcfromtimestamp]))
    ])

method_properties |= set([year, month, day, hour, minute, second, millisecond,
                          microsecond, date, time, utcfromtimestamp])
