"""
Calculate the angle from north, given two geodetic coordinates.

Attribution:
https://gist.github.com/jeromer/2005586
"""


import math


def azimuth(lon1, lat1, lon2, lat2):
    """
    Calculates the bearing between two points.

    :Parameters:
      - `pointA`=(lon1, lat1):
        The tuple representing the latitude/longitude for the first point.
        Latitude and longitude must be in decimal degrees
      - `pointB`=(lon2,lat2):
        The tuple representing the latitude/longitude for the second point.
        Latitude and longitude must be in decimal degrees
    :Returns:
      Clockwise angle (in degrees) from the north-vector centred at (lon1, lat1)
      to the line from (lon1, lat1) to (lon2, lat2). Angle is in range [0, 360).
    :Returns Type:
      float
    """
    pointA, pointB = [(lat1, lon1), (lat2, lon2)]
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    if initial_bearing < 0:
        initial_bearing = 360 + initial_bearing

    return initial_bearing


print "north        ", azimuth(lon1=0, lat1=0, lon2=0, lat2=3)
print "northeast    ", azimuth(lon1=0, lat1=0, lon2=3, lat2=3)
print "east         ", azimuth(lon1=0, lat1=0, lon2=3, lat2=0)
print "south        ", azimuth(lon1=0, lat1=0, lon2=0, lat2=-3)
print "west         ", azimuth(lon1=0, lat1=0, lon2=-3, lat2=0)
print "northwest    ", azimuth(lon1=0, lat1=0, lon2=-3, lat2=3)