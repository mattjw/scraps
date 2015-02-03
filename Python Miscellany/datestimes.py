# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     2015
# License:  MIT License

"""
Various functions for handling date and time.
"""


def secs_to_str(total_secs):
    """
    Convert a number of seconds `totsecs` (total seconds) to a string.
    The string is formatted in terms of days, hours, minutes, and seconds.
    Fractions of a second are represented by a decimal number of seconds.
    Values are only printed from the leading non-zero denomination.
    
    Examples::

    >>> secs_to_str(0)
    '0.0s'
    >>> secs_to_str(60)
    '1m 0.0s'
    >>> secs_to_str(60*60)
    '1h 0m 0.0s'
    >>> secs_to_str(60*60*24)
    '1d 0h 0m 0.0s'
    >>> secs_to_str(60*60*24+8324.65)
    '1d 2h 18m 44.65s'
    """
    if total_secs < 0:
        raise ValueError("Total seconds (%s) must be 0 or greater" % totsecs)
    denoms = [(24*60*60, 'd'), (60*60, 'h'), (60, 'm')]
    rem = float(total_secs)
    keep = False
    text = ""
    for weight, symb in denoms:
        val = rem // weight
        if val > 0:
            keep = True
        if keep:
            text += "%02d%s " % (val, symb)
        rem = rem % weight
    text += "%06.03fs" % rem
    return text


def dt_floor(dt, magnitude='day'):
    """
    Floor a datetime according to a given magntiude.

    For example,
        dt_floor(datetime(2014, 2, 28, 13, 30), magnitude='day'),
    will return the datetime floored to the lowest day:
        datetime(2014, 2, 28, 0, 0).

    Permitted magnitudes are:
        'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond'

    :Return:
    The floor of `dt` with respect to magnitude `magnitude`.
    """
    mags = ('year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond')
    subs = ( None,   1,       1,     0,      0,        0,        0)

    if magnitude not in mags:
        raise ValueError("Unknown magnitude '%s'; choose from: %s" % (magnitude, ', '.join(mags)))

    replace_from = mags.index(magnitude)
    for indx in xrange(replace_from+1, len(mags)):
        mag = mags[indx]
        sub = subs[indx]
        arg = {mag: sub}
        dt = dt.replace(**arg)
    return dt