# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     2015
# License:  MIT License

# Version: 0.0.1
#          28 May 2016
#
# Future improvements:
# * Check how well this handles DST shifts.


import collections
import pandas as pd
import datetime


class TimeSeriesBuilder(object):
    """
    Simple helper for constructing a time series of counts (tweet volume,
    checkin volume, etc.). Does not require a priori knowledge of observation
    period.

    Example use case #1:
    You have a large file containing tweets, and you want to count the number
    of tweets in each hour. The observation period is not known beforehand.
    You just want to read in the series of tweets and track the number of
    tweets per hour.

    Example use case #2:
    As with #1, except you want to only track the number of (unique) users
    who've tweeted in each hour.
    """

    def __init__(self, bucket_width_mins=60):
        if int(bucket_width_mins) != bucket_width_mins:
            raise ValueError("Bucket width must be int")
        bucket_width_mins = int(bucket_width_mins)

        if bucket_width_mins == 0:
            raise ValueError("Bucket width must be positive")
        if bucket_width_mins > 60:
            raise ValueError("Bucket width must be no greater than 60 mins")
        if (60 % bucket_width_mins) != 0:
            raise NotImplementedError("Bucket width must be divisor of 60 minutes")

        self._counts = collections.defaultdict(lambda: 0.0)
        self._uniqs = collections.defaultdict(lambda: set())
        self._bucket_width_mins = bucket_width_mins

    def increment_at(self, dt, obj=None):
        """
        Increment the count at time `dt`.
        If `obj` is not None, the count is only incremented if `obj` has not
        been seen in this timestep before.
        """
        if self._bucket_width_mins == 60:
            dt = dt.replace(minute=0, second=0, microsecond=0)
        elif 1 <= self._bucket_width_mins <= 60:
            #print "~", dt,
            mins = dt.minute
            floored = (mins // self._bucket_width_mins) * self._bucket_width_mins
            dt = dt.replace(minute=floored, second=0, microsecond=0)
            #print " -> ", dt, "\n"
        else:
            assert False

        assert dt.tzinfo is not None

        if obj is not None:
            if obj in self._uniqs[dt]:
                return
            else:
                self._uniqs[dt].add(obj)

        self._counts[dt] += 1.0

    def to_series(self):
        """
        Empty Series if no samples received.
        """
        if len(self._counts) == 0:
            return pd.Series()

        min_dt = min(self._counts.iterkeys())
        max_dt = max(self._counts.iterkeys())
        assert min_dt.tzinfo is not None

        td_buck = datetime.timedelta(minutes=self._bucket_width_mins)

        dt_seq = []
        counts_seq = []
        dt = min_dt
        while dt <= max_dt:
            dt_seq.append(dt)
            counts_seq.append(self._counts[dt])
            dt += td_buck

        ser = pd.Series(index=dt_seq, data=counts_seq)
        ser.index.name = 'snapshot'
        #ser = ser.to_period('H')  # DatetimeIndex -> PeriodIndex. Datetime is better; retains tzoffset
        assert ser.sum() == sum(self._counts.itervalues()), [ser.sum(), sum(self._counts.itervalues())]
        return ser


def main():
    from datetime import datetime
    import pytz

    tz = pytz.utc
    
    vts = TimeSeriesBuilder()
    print vts.to_series()

    mins = 3

    vts = TimeSeriesBuilder(mins)
    vts.increment_at(datetime(2016, 1, 1,  7, 11, 30, 4, tzinfo=tz))
    vts.increment_at(datetime(2016, 1, 1,  8, 30, tzinfo=tz))
    vts.increment_at(datetime(2016, 1, 1,  8, 45, tzinfo=tz))
    vts.increment_at(datetime(2016, 1, 1,  8, 47, tzinfo=tz))
    vts.increment_at(datetime(2016, 1, 1,  9, 00, tzinfo=tz))
    print vts.to_series()

    vts = TimeSeriesBuilder(mins)
    vts.increment_at(datetime(2016, 1, 1,  8, 0, tzinfo=tz), "a")
    vts.increment_at(datetime(2016, 1, 1,  8, 30, tzinfo=tz), "a")
    vts.increment_at(datetime(2016, 1, 1,  8, 45, tzinfo=tz), "a")
    vts.increment_at(datetime(2016, 1, 1,  9, 00, tzinfo=tz), "a")
    print vts.to_series()


if __name__ == "__main__":
    main()



