# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     2015
# License:  MIT License


import math
import numpy as np


"""
Compute the centroid of a set of vertices on the Earth's surface. This is also
sometimes called the mid-point or center of mass of the set of points.

More formally, we compute the MEAN CENTROID of the set of points. The set
of points is interpreted purely as a set of points, not a polygon, hull,
edge set, or other.

There are many notions of the 'mid point' of a set of vertices. These include
center of mass, center of gravity, and center of minimum distance. This
module provides a variety of methods for computing the same concept of a
centroid, which we define as the mean position of all the coordinate dimensions.
This module specifically handles computing the centroid for points lying on
the surface of the Earth, which requires adjustment for its elliptical nature.

Our definition of centroid is also called the geometric center. Since we assume
uniform density and weight across points and positions on the surface of the
Earth, this measure is equivalent to both the center of mass and the center of
gravity of the point set.

Note that the centroid is not the center of minimum distance. The centroid is
related to the mean as it minimises the sum of squared distances. On the other
hand, the center of minimum distance is related to the median as it minimises 
the sum of absolute distances.

Four methods for computing the (same) centroid are provided. These vary in the
accuracy of their result. The methods, ranked with most-accurate first, are as
follows:
 1. centroid_wgs84:
    Accurately models the ellipsoid shape of the Earth.
 2. centroid_sphere:
    Small error introduced by purely spherical interpretation.
 3. centroid_planar:
    Projecting on to a flat surface introduces significant errors over large
    distance.
 4. centroid_geodetic_mean:
    Takes the mean of the spherical coordiantes. Oblivious to the shape of the
    Earth. Very large errors introduced for sets that are scattered around the
    international date line, as this method is oblivious to the true distance
    between longitude +179.0 vs longitude -179.0.

Conventions used in this module are as follows...

Spherical geographic coordinate system ['spherical']:
    lambda   longitude
    phi      latitude
Given as (longitude, latitude) pairs. Equivalently denoted by (lambda, phi).
Units are degrees.
(0,0)  = prime meridian at the equator
(0,90) = north pole

radius of earth r

Euclidian space embedding ['cartesian']:
We model the Earth as a sphere inscribed in a cuboid.
Three dimensional euclidian space. x axis cuts through (0,0). xy plane
splits the Earth through the equator.
<0,0,0> = center of earth
<r,0,0> = prime meridian at the equator
<0,0,r> = north pole
Untis are kilometres.
"""


#
#
# SPHERE
# Model Earth as a perfect sphere.
#

EARTH_RADIUS_KM = 6372.795


def spherical_to_cartesian(longitude, latitude, r=EARTH_RADIUS_KM):
    """
    Convert a point in spherical coordinates (`longitude`, `latitude`) to
    three-dimensional Cartesian coordinates.

    Assumes spherical (non-ellipsoid) earth.

    :Params:
    longitude, latitude:
        Geographic spherical coordinates, in degrees.
    
    :Returns:
    Cartesian coordinates as (x,y,z). In km.
    """
    lambd = math.radians(float(longitude))
    phi = math.radians(float(latitude))

    x = r * math.cos(phi) * math.cos(lambd)
    y = r * math.cos(phi) * math.sin(lambd)
    z = r * math.sin(phi)
    return (x, y, z)


def cartesian_to_spherical(x, y, z):
    """
    Convert a point in Cartesian coordinates (`x`, `y`, `z`) to spherical
    coordinates.

    Assumes spherical (non-ellipsoid) earth.

    :Params:
    Cartesian coordinates as (x,y,z). In km.
    
    :Returns:
    (longitude, latitude)
    Geographic spherical coordinates, in degrees.
    """
    x, y, z = map(float, [x, y, z])

    r = math.sqrt(x**2 + y**2 + z**2)

    # in two steps...
    # 1. given xy plane location, find hypotenuse on xy plane from x and y
    hyp = math.sqrt(x**2 + y**2)
    lambd = math.atan2(y, x)  # lambd = math.acos(x / hyp) = math.atan2(y, x)

    # 2. use hypotenuse and z-value to compute phi
    phi = math.atan2(z, hyp)

    # convert back
    longitude = math.degrees(lambd)
    latitude = math.degrees(phi)
    return (longitude, latitude)


def centroid_sphere(longlat_pairs):
    """
    Compute the centroid of a set of vertices (`longlat_pairs`) on the earth's 
    surface. Coordiantes of the vertices in geographic spherical coordiantes;
    i.e., as long, lat coordiantes.

    This computation is smarter than naive averaging of the long, lat
    coordiantes. The centroid is computed in three-dimensional euclidian space,
    and then converted back to spherical coordiantes by projecting out of the
    center of the earth (ray-sphere intersection).

    Assumes a spherical (non-ellipsoid) Earth.

    :Params:
    `longlat_pairs`: A sequence of points as (long, lat) coordinates.

    :Returns:
    Centroid of `longlat_pairs`, as long-lat pair.
    """
    # sphere embedded in cuboid. convert spherical to cartesian
    N = len(longlat_pairs)
    cartesians = np.zeros([N, 3])  # N-high, 3-wide
    for indx, pair in enumerate(longlat_pairs):
        lng, lat = map(float, pair)
        coords = spherical_to_cartesian(lng, lat)
        cartesians[indx,:] = coords

    # centroid by mean of each dimension
    # note: this will now be below the earth's surface (i.e., magnitude of this
    # x, y, z is less than EARTH_RADIUS_KM). Becuase we assume spherical
    # (not ellipsoid) earth, this magnitude will not affect the spherical 
    # coordinates returned
    centr = np.average(cartesians, axis=0)

    if np.all(centr==0):
        raise ValueError("This pointset yields non-unique centroid")  # multiple solutions

    # obtain spherical coordinates
    lng, lat = cartesian_to_spherical(*centr[:])
    return (lng, lat)


#
#
# ELLIPSOID (WGS 84)
# Model Earth as an WGS84 ellipsoid.
#

def centroid_wgs84(longlat_pairs):
    """
    Compute accurate centroid of a set of geodetic coordinates (long-lat pairs)
    via Cartesian space while modelling Earth as a WGS-84 ellipsoid.

    :Params:
    `longlat_pairs`: A sequence of points as (long, lat) coordinates.

    :Returns:
    Centroid of `longlat_pairs`, as long-lat pair.
    """
    import pysatel
    # altitude:
    # elevation above the surface of the spheroid; i.e., altitude above the
    # surface
    # http://en.wikipedia.org/wiki/Reference_ellipsoid#Coordinates
    #   "The coordinates of a geodetic point are customarily stated as geodetic
    #   latitude and longitude, i.e., the direction in space of the geodetic
    #   normal containing the point, and the height h of the point over the
    #   reference ellipsoid.""
    # http://www.oc.nps.edu/oc2902w/coord/coordcvt.pdf
    #   convention here is that height is the distance over the surface (see diagram)
    # http://www.esri.com/news/arcuser/0703/geoid1of3.html
    #   includes excellent diagram
    #   The traditional, orthometric height (H) is the height above an imaginary surface called the geoid
    #   The GPS uses height (h) above the reference ellipsoid that approximates the earth's surface.

    N = len(longlat_pairs)

    cartesians = np.zeros([N, 3])  # N-high, 3-wide
    for indx, pair in enumerate(longlat_pairs):
        lng, lat = map(float, pair)
        coords = pysatel.geodetic2ecef(lat, lng, alt=0.0)
        cartesians[indx,:] = coords

    centr = np.average(cartesians, axis=0)

    if np.all(centr==0):
        raise ValueError("This pointset yields non-unique centroid")  # multiple solutions

    lat, lng = pysatel.ecef2geodetic(*centr[:])

    return (lng, lat)


#
#
# NAIVE -- MEAN OF SPHERICAL COORDINATES
#

def centroid_geodetic_mean(longlat_pairs):
    a = np.array(longlat_pairs)
    cent = np.average(a, 0)
    return cent


#
#
# PLANAR PROJECTION
# Project surface of the Earth on to a flat (2d) surface.
#

def centroid_planar(longlat_pairs):
    """
    Centroid by projecting onto a plane. Inaccurate over long distances.
    """
    #
    # projections prep
    from pyproj import Proj, transform
    p_geodetic = Proj(proj='latlong')
    p_flat = Proj('+init=EPSG:27700')  # uk OS

    #
    # convert
    N = len(longlat_pairs)

    cartesians = np.zeros([N, 2])  # N-high
    for indx, pair in enumerate(longlat_pairs):
        lng, lat = map(float, pair)
        x, y = transform(p_geodetic, p_flat, lng, lat)
        cartesians[indx,:] = (x, y)

    x, y = np.average(cartesians, axis=0)

    lng, lat = transform(p_flat, p_geodetic, x, y)

    return (lng, lat)


if __name__ == "__main__":
    import geopy.distance



    def __dist_great_circle(loc1, loc2):
        """
        Assumed that the input locations are represented as (long, lat) pairs.

        :Params:
        loc1 = (long, lat)

        Returns distance in metres.
        """
        # great circle (haversine) is good enough for Fortunato
        # http://geopy.readthedocs.org/en/latest/index.html?highlight=great%20circle#geopy.distance.great_circle
        # cleveland_oh = (41.499498, -81.695391)    =>   lat, long
        l1 = (loc1[1], loc1[0])
        l2 = (loc2[1], loc2[0])
        dist_km = geopy.distance.great_circle(l1, l2).km
        dist_m = dist_km * 1000.0
        return dist_m

    #
    #
    # Test spherical -> cartesian -> spherical conversion
    #

    def test(desc, lng, lat):
        print desc
        sph1 = (lng, lat)
        cart = spherical_to_cartesian(*sph1)
        sph2 = cartesian_to_spherical(*cart)
        print "\t%-20s%s" % ("spherical", (sph1))
        print "\t%-20s%s" % ("cartesian", (cart))
        print "\t%-20s%s" % ("spherical", (sph2))
        print

    test('meridian-equator', 0, 0)
    test('meridian-equator +90long', 90, 0)
    test('north pole', 0, 90)
    test('south pole', 0, -90)

    
    #
    #
    # Test centroid computation
    #

    def total_abs_error(cent, longlats):
        # returns total distance errors, in km
        err = 0.0
        for p in longlats:
            err += __dist_great_circle(cent, p) / 1000.0
        return err

    def root_sq_error(cent, longlats):
        # returns total distance errors, in km
        err = 0.0
        for p in longlats:
            err += (__dist_great_circle(cent, p) / 1000.0)**2.0
        err = err**(0.5)
        return err

    def test(desc, pairs):
        print
        print
        print desc.upper()

        print "set of longlats:"
        for p in pairs:
            print "\t", p

        print "centroid (non-ellipsoid)"
        cent = centroid_sphere(pairs)
        print "\t(%.4f,%.4f)    \ttotal abs error: %.3f" % (cent[0], cent[1], total_abs_error(cent, pairs))
        print "\t\t               root squared error: %.1f" % (root_sq_error(cent, pairs))

        print "true center-of-min-dist for Cdf-Prs-Msc example"
        cent = (2.356, 49.602)
        print "\t(%.4f,%.4f)    \ttotal abs error: %.3f" % (cent[0], cent[1], total_abs_error(cent, pairs))
        print "\t\t               root squared error: %.1f" % (root_sq_error(cent, pairs))

        print "wgs84 centroid"
        cent = centroid_wgs84(pairs)
        print "\t(%.4f,%.4f)    \ttotal abs error: %.3f" % (cent[0], cent[1], total_abs_error(cent, pairs))
        print "\t\t               root squared error: %.1f" % (root_sq_error(cent, pairs))

        try:
            print "via flat projection"
            cent = centroid_planar(pairs)
            print "\t(%.4f,%.4f)    \ttotal abs error: %.3f" % (cent[0], cent[1], total_abs_error(cent, pairs))
            print "\t\t               root squared error: %.1f" % (root_sq_error(cent, pairs))
        except RuntimeError:
            pass

        print "naive centroid"
        cent = centroid_geodetic_mean(pairs)
        print "\t(%.4f,%.4f)    \ttotal abs error: %.3f" % (cent[0], cent[1], total_abs_error(cent, pairs))
        print "\t\t               root squared error: %.1f" % (root_sq_error(cent, pairs))
        


    test("example: Cardiff-Birmingham-Greenwich triangle",
            [
            (-3.1833, 51.4833), # cardiff
            (-1.8936, 52.4831), # birmingam
            (0.0, 51.4800), # greenwich
            ])

    test("example: Cardiff-Paris-Moscow triangle",
            [
            (-3.1833, 51.4833), # cardiff
            (2.3508, 48.8567), # paris
            (37.6167, 55.7500), # moscow
            ])

    test("example: Anchorage-Seoul-Tokyo (across IDL)",
            [
            (-149.9000, 61.2167),
            (126.9781, 37.5667),
            (139.6917, 35.6895),
            ])

    test("example: Greenwich, above and below",
            [
            (0.1, 51.4800),
            (0.0, 50.4800),
            (0.1, 52.4800)
            ])

    test("example: (almost) opposing sides",
        [
        (-89.0, 0.0),
        (89.0, 0.0),
        ])

    # summary:
    #
    # wrt finding the center of minimum distance...
    # * Our approach always minimises the average distance better than
    #   the naive centroid method (average the spherical coords)
    #
    # * The naive centroid approach is inconsistent when dealing with the 
    #   international date line. Our approach is consistent. 
    #   Points over any region of the earth are computed correctly, regardless
    #   of IDL.

    # useful resources:
    #
    # excellent discussion of the meaning of 'centroid' for points, polygons,
    # etc.:
    # http://gis.stackexchange.com/questions/22739/how-to-find-the-center-of-geometry-of-an-object/22744#22744
    # 
    # interactive tool and various computation approaches...
    # http://www.geomidpoint.com/
    #
    # discussion of using the euclidian space approach...
    # http://gis.stackexchange.com/questions/6025/find-the-centroid-of-a-cluster-of-points#comment6614_6026
    