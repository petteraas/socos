""" various utility functions """

import re
from inspect import getargspec
from functools import wraps
import soco

# matches single numbers ("123") or ranges ("12..34")
RANGE_PATTERN = re.compile(r'(\d+)(..(\d+))?')


def parse_range(txt):
    """ Matches a single number A or a range of two numbers A..B

    The range A..B is interpreted as including both A and B

    >>> list(parse_range('123'))
    [123]

    # comparing range objects is not possible in Python 3.2
    >>> list(parse_range('12..34')) == list(range(12, 35))
    True
    """

    matches = RANGE_PATTERN.match(txt)

    if not matches:
        raise ValueError('Invalid number or range: "{}"'.format(txt))

    # the first number is always matched
    val1 = int(matches.group(1))

    # group(2) is "..val2", group(3) is "val2"
    if matches.group(3) is not None:
        val2 = int(matches.group(3))
    else:
        # no second number, so we need a range of length 1
        val2 = val1

    return range(val1, val2+1)


def requires_coordinator(func):
    """
    A decorator to mark functions requiring a
    group coordinator device.
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        """
        Wrap a function, find the sonos argument to it
        and turn it into a sonos.group.coordinator
        before running the original function
        """

        argspec = getargspec(func)
        sonos = args[argspec.args.index('sonos')]

        args = list(args)

        if isinstance(sonos, soco.SoCo):
            args[argspec.args.index('sonos')] = sonos.group.coordinator

        return func(*args, **kwargs)
    return decorated
