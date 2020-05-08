# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     2014
# License:  MIT License
#           http://opensource.org/licenses/MIT

"""
A decorator for tenacious HTTP querying.

Wrap a function in this decorator to have it automatically re-executed in case
of an HTTP error. The decorator implements progressive backoff to avoid
hammering the server.

Built for HTTP requests issued via the `requests` library.
See: http://python-requests.org

The function being decorated should issue an HTTP query via the requests
library, and should return the corresponding `requests.Response` object.
"""

__author__ = "Matt J Williams"
__author_email__ = "mattjw@mattjw.net"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2014 Matt J Williams"


import time

import requests
import urllib3


DEFAULT_RETRY_STATUS_CODES = [429, 502, 503]
DEFAULT_MAX_BACKOFF = 30.0
DEFAULT_BACKOFF_MULTIPLIER = 1.5
DEFAULT_INITIAL_BACKOFF = 0.3
DEFAULT_RETRY_EXCEPTIONS = (requests.exceptions.Timeout,
                            requests.exceptions.ConnectionError,
                            urllib3.exceptions.ProtocolError)


class tenacious(object):
    """
    Decorate a function that issues and returns an HTTP query via the requests
    library. Querying is carried out tenaciously; i.e., if the function fails
    due to a transient HTTP issue, it will backoff and keep tryin. The
    decorated function will only return the result of a successful query.

    The query time (i.e., HTTP roundtrip) is included in the backoff
    duration.

    The decorator uses reasonable defaults are provided for all parameters, but 
    these can be customised as follows.
    `retry_status_codes`:
        A list of HTTP status codes that should trigger a retry. See below.
    `max_backoff`:
        The maximum duration between retries. In seconds.
    `backoff_multiplier`:
        The factor that the backoff duration should be multiplied by between
        retries. This results in the backoff being progressively increased, up
        to the maximum `max_backoff`.
    `initial_backoff`:
        The backoff to be used after the first failed query. In seconds.

    The following is a list HTTP response status codes are regarded as requiring
    a re-query. Typical causes for these errors are also included.
    * 429 Too Many Requests. The server is over-capacity.
    * 502 Bad Gateway. A service or server that the target server depends on is
      having issues. Some servers also use this to represent over-capacity
      errors; e.g., Twitter's famous Fail Whale.
    * 503 Service Unavailable. The server may be down for maintenance.
    These are default codes chosen as they are typically transient errors. The
    list can be customised.

    The following exceptions also trigger a re-query:
    * requests.exceptions.Timeout
    * requests.exceptions.ConnectionError
    * urllib3.exceptions.ProtocolError
    """

    # ivars:
    #
    # self.__next_query_time
    # the time at which the next query should be issued. in reality, this is
    # the *earliest* time at which the next query should be issued.
    #
    # self.__next_backoff
    # if the next query is a failure, this is how much time the function should
    # wait after this failed query. this will not be greater than the
    # max backoff.

    def __init__(self,
                 retry_status_codes=DEFAULT_RETRY_STATUS_CODES,
                 max_backoff=DEFAULT_MAX_BACKOFF,
                 backoff_multiplier=DEFAULT_BACKOFF_MULTIPLIER,
                 initial_backoff=DEFAULT_INITIAL_BACKOFF):

        if not (max_backoff >= 0):
            raise ValueError("Maximum backoff (%s) should not be below zero" % max_backoff)

        if not (backoff_multiplier >= 1):
            raise ValueError("Backoff multiplier (%s) must not result in decreasing backoffs" % backoff_multiplier)

        if not (initial_backoff >= 0):
            raise ValueError("Initial backoff (%s) must not be below zero" % initial_backoff)

        self.__retry_status_codes = retry_status_codes
        self.__max_backoff = max_backoff
        self.__backoff_multiplier = backoff_multiplier
        self.__initial_backoff = initial_backoff

        self.__next_query_time = time.time()
        self.__next_backoff = self.__initial_backoff  # duration of the next backoff

    def __call__(self, func, *args, **kwargs):
        def tenacious_wrapper(*args, **kwargs):
            while True:
                #
                # Backoff (if any)
                sleep_dur = self.__next_query_time - time.time()
                if sleep_dur >= 0:
                    time.sleep(sleep_dur)  # may raise signals

                #
                # Exec query
                try:
                    response = func(*args, **kwargs)

                    if not (response.status_code in self.__retry_status_codes):
                        # successful query!
                        return response
                    else:
                        # later, we'll need to trigger a retry
                        pass
                except DEFAULT_RETRY_EXCEPTIONS as ex:
                    # later, we'll need to trigger a retry
                    pass

                #
                # The query was a failure. Let's backoff and try again
                backoff_dur = self.__next_backoff
                self.__next_query_time = time.time() + backoff_dur

                self.__next_backoff = min([backoff_dur * self.__backoff_multiplier,
                                           self.__max_backoff])

        return tenacious_wrapper


if __name__ == "__main__":

    import random

    global stamp
    stamp = time.time()
    print "%-30s\t%s" % ("time at exec:", stamp)

    @tenacious()
    def testfunc1():
        global stamp
        print "%-30s\t%s\t(%s)" % ("next stamp:", stamp, time.time()-stamp)
        stamp = time.time()


        if random.random() <= 0.05:
            # valid query (200 status) 5% of the time
            url = "http://www.random.org/integers/?num=10&min=1&max=6&col=1&base=10&format=plain&rnd=new"
        else:
            # invalid query (503 error) the rest of the time
            url = "http://www.random.org/integers/?num=10&min=1&max=6&col=1&base=-1&format=plain&rnd=new"

        try:
            resp = requests.get(url)
            ex = None
        except Exception as ex:
            resp = None
        
        if ex is not None:
            raise ex
        else:
            return resp

    testfunc1()

    print "%-30s\t%s\t(%s)" % ("time at complete:", stamp, time.time()-stamp)
    stamp = time.time()










