# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     2015
# License:  MIT License
#           http://opensource.org/licenses/MIT


"""
Decordators for memoisation, including in-memory memoisation and persistent
(on-disk) memoisation. Similar to an LRU cache (last-recently used).
"""

import cPickle as pickle
import os.path
import collections

__author__ = "Matt J Williams"
__author_email__ = "mattjw@mattjw.net"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2015 Matt J Williams"


class persistent_memoisation(object):
    """
    A memoiser that stores its cache in a file on disk, allowing persistence of
    memoisation between multiple executions of the same script.

    ~todo~

    Internally, we represent the cache as a dict. The lookup is of the form:
        dict[(args, kwargs)] = result
    where args is the sequence of *args and kwargs is a frozenset representing
    key-value pairs from **kwargs.
    """

    def __init__(self, cache_fpath):
        """
        ~todo~
        """
        self.__cache_fpath = cache_fpath
        if os.path.exists(cache_fpath):
            if not os.path.isfile(cache_fpath):
                raise ValueError("'%s' exists but is not a file" % (cache_fpath))

            with open(cache_fpath, 'r') as f:
                obj = pickle.load(f)
                if not isinstance(obj, dict):
                    # note: OrderedDict inherits from dict
                    raise ValueError("Expected a dict")
                self.__cache = obj
        else:
            with open(cache_fpath, 'w') as f:
                self.__cache = collections.OrderedDict()
                self.__write_cache()  # self.__cache will be written to the cache file

    def __write_cache(self):
        """
        Write whatever is stored in the cache (`self.__cache`) to the cache file
        (at filepath `self.__cache_fpath`).
        """
        with open(self.__cache_fpath, 'w') as f:
            pickle.dump(self.__cache, f)

    def __call__(self, func, *args, **kwargs):
        """
        ~todo~
        """
        def tenacious_wrapper(*args, **kwargs):
            # Attempt to satisfy the call via the cache
            key = (args, frozenset(kwargs.items()))
            if key in self.__cache:
                return self.__cache[key]

            # Need to compute
            result = func(*args, **kwargs)

            # Add to cache and write it out
            self.__cache[key] = result
            self.__write_cache()

            return result
        return tenacious_wrapper


if __name__ == "__main__":
    import numpy as np

    @persistent_memoisation(cache_fpath="./test.pkl")
    def interval_mean(a, b, nsamps=4 * 10**7):
        # Return the mean value in the interval [a, b]
        # Dumbly use Monte Carlo simulation to do this, which is intended to be
        # expensive
        arr = a + (np.random.sample(nsamps) * float(b-a))
        mean = np.mean(arr)
        return mean

    a = 0

    print "\nbatch 1"
    for b in xrange(0, 4):
        print "[%s,%s] \t " % (a,b), interval_mean(a, b)

    print "\nbatch 2"
    for b in xrange(0, 8):
        print "[%s,%s] \t " % (a,b), interval_mean(a, b)

    print "\nbatch 3"
    for b in xrange(0, 12):
        print "[%s,%s] \t " % (a,b), interval_mean(a, b)

    print "\nre-run with different kwarg"
    nsamps = 3 * 10**7
    for b in xrange(0, 12):
        print "[%s,%s] (%s) \t " % (a, b, nsamps), interval_mean(a, b, nsamps=nsamps)

    print "\nre-run with different kwarg"
    nsamps = 1
    for b in xrange(0, 12):
        print "[%s,%s] (%s) \t " % (a, b, nsamps), interval_mean(a, b, nsamps=nsamps)



