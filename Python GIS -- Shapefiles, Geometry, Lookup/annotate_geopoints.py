# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     2015
# License:  MIT License
#           http://opensource.org/licenses/MIT

"""
Annotate a list of geographic locations (as latitudes and longitudes) with
geographic information about the regions they belong to.

Inputs:
* GEOPOINTS:
    CSV file of geopoints.
    Each row represents a geographic location. The position is represented
    by longitude and latitude. Each row may also contain other information
    about the location. Thus, we have "locations" and their "input labels".
* REGION SHAPES:
    Region spatial data.
    The boundaries of a set of geographic regions. The GEOPOINTS exists within
    one of these spatial regions.
* REGION ATTRIBUTES:
    CSV file containing additional attributes for the regions described in
    REGION SHAPES.
    Each row should match to an ID of a region in REGION SHAPES.

Outputs:
Each GEOPOINT is annotated with attributes (REGION ATTRIBUTES) of the region it
belongs to (REGION SHAPES).
"""
# Computational geometry, polygon lookup, point lookup, polygon locator
# pysal.cg.locators.PolygonLocator(polygons)
#   contains_point(point)
#     Returns polygons that contain point
#https://pysal.readthedocs.org/en/latest/library/cg/locators.html

__author__ = "Matt J Williams"
__author_email__ = "mattjw@mattjw.net"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2015 Matt J Williams"


import collections
import csv
import math

from shapefile_tools import polygon_shaperecords
import pysal
from pysal.cg.locators import PolygonLocator
import pyproj


#
#
# Params
#

# GEOPOINTS file
fpath_geopoints = "dat/foodvenues_london.csv"
geopoints_lat_col = 2
geopoints_lon_col = 3
    # latidue and longitude columns in the GEOPOINTS file
    # index from 0

# REGION ATTRIBUTES files
fpath_region_attribs = "dat_imd/imd2010.csv"
region_attribs_id_col = 0
    # the column in the REGION ATTRIBUTES file that contains the region identifier
    # cross-referenced with the region id in REGION SHAPES

# REGION SHAPES file
fpath_region_shapes = "dat_lsoa/LSOA_2004_London_Low_Resolution"
region_shape_fieldname = 'LSOA_CODE'
fpath_region_shapes = "dat_lsoa/LSOA_2001_EW_BGC_V2"
region_shape_fieldname = 'LSOA01CD'
    # the fieldname of the shape attribute in the REGION SHAPES file
    # that has the shape identifier
    # cross referenced with the id in REGION ATTRIBTUES

# OUTPUT file
fpath_output = 'dat/annotated.csv'
fpath_output_no_region = 'dat/no_region.csv'


#
#
# Script
#

def get_regions():
    regions = {}
        # maps a pysal polygon to the input shapedict,
        # inc. pyshp geometry and shapely geometry

    for indx, shape_dict in enumerate(polygon_shaperecords(fpath_region_shapes)):
        # 'geom_pyshp', 'geom_shapely', ...
        geom_shapely = shape_dict['geom_shapely']
        geom_pysal = pysal.cg.asShape(geom_shapely)

        if region_shape_fieldname not in shape_dict:
            raise ValueError("'%s' not in shape file %s" % (region_shape_fieldname, shape_dict.keys()))

        regions[geom_pysal] = shape_dict
    return regions


def get_region_attributes():
    region_attribs = {}
        # maps a region ID to an ordered dictionary of attributes
        # regarding that reigon
        # the ID *is* still included in the ordered dictionary

    with open(fpath_region_attribs, 'rU') as fin:
        rdr = csv.reader(fin)
        fnames = rdr.next()
        ident_colname = fnames[region_attribs_id_col]
        for row in rdr:
            dct = collections.OrderedDict(zip(fnames, row))

            # retrieve the ID
            ident = dct[ident_colname]
            region_attribs[ident] = dct

    return region_attribs


def extract_geopoint_location(geopoint_row):
    """
    Extract location data from a geopoint row (a row in GEOPOINTS) and
    normalise its format (e.g., from lat-long) to the same format that is used
    by the region shape data (i.e., REGION SHAPES).

    For example, the region geometries might be provided in BNG (British
    National Grid) format, and the geopoints might be described as long lat.
    This function would extract the geopoint's long-lat pair and 
    transform them to BNG for comparison with the region gemoetries.
    """
    wgs84 = pyproj.Proj(init='epsg:4326')  # wgs is a geodetic coordinate system
    bng = pyproj.Proj(init='epsg:27700')  # UK LSOA are in BNG (british nat grid)

    lon = float(geopoint_row[geopoints_lon_col])
    lat = float(geopoint_row[geopoints_lat_col])

    bng_east, bng_north = pyproj.transform(wgs84, bng, lon, lat)
    loc = (bng_east, bng_north)
    return loc


def save_dict_seq(seq, fpath):
    """
    Save a sequence of dics `seq` to file at path `fpath` in CSV format.
    Header will be inferred fro mthe dict keys.
    """
    if len(seq) == 0:
        raise ValueError("Cannot save empty sequence")

    with open(fpath, 'w') as f:
        fnames = seq[0].keys()
        wrtr = csv.DictWriter(f, fnames)
        wrtr.writeheader()
        wrtr.writerows(seq)


def loc_to_region_attribs(loc, regions, region_locator, region_attribs,
        nearest_fuzzy=False):
    """
    Find the region for the point `loc` and return its region attributes.
    Returns a dictionary of region attributes.

    Preferentially tries to find the region that contains `loc`. 

    ==NOT IMPLEMENTED YET==
    If nearest_fuzzy is True, then also attempt 'fuzzy nearest polygon' 
    search after a failed containment check. This will try and use the 
    nearest polygon to the point. A crude sanity check is also included to
    ensure that (relatively) distance polygons are not matched.
    (Waiting for 'nearest' to be implemented in PySAL.
    See: http://pysal.readthedocs.org/en/latest/library/cg/locators.html)
    ====

    Params...
    loc:
        Location.
    regions:
        Dictionary that allows lookup of PySAL shape objects to their
        region shape information.
    region_locator:
        Lookup PySAL polygon to region attributes.
    region_attribs:
        Dictionary lookup that maps region ID to region attrinutes.

    Returns None if no region found.
    Throws error if multiple polygons match.
    """
    match = None  # the polygon successfully matched to this region

    #
    # First try containment
    polys = region_locator.contains_point(loc)
        # list of geom_pysal polygons

    if len(polys) > 1:
        raise RuntimeError("multiple polygons for %s" % loc)

    if len(polys) == 1:
        match = polys[0]

    #
    # Attempt fuzzy nearby matching, if enabled
    if nearest_fuzzy and (match is None):
        poly = region_locator.nearest(loc)
        # approximate 'diameter' of the shape as if it were a circle
        diam = math.sqrt(poly.area / math.pi)
        dist = pysal.cg.standalone.get_polygon_point_dist(poly, loc)
            # presumably the distance to the nearest border?
        if dist <= (0.05 * diam):
            # i.e., the distance from the point to the polygon is
            # less than 5% of the 'diameter' of the polygon
            print "matched within 5%"
            match = poly

    #
    # Check if poly-finding worked
    if match is None:
        return None

    #
    # Resolve the attributes for this polygon
    region_dct = regions[match]
    region_id = region_dct[region_shape_fieldname]
    attribs_dct = region_attribs[region_id]
    return attribs_dct


if __name__ == "__main__":

    print "[Load REGION SHAPES]"
    regions = get_regions()
    region_locator = PolygonLocator(regions.iterkeys())

    print "[Load REGION ATTRIBUTES]"
    region_attribs = get_region_attributes()

    print "[Process GEOPOINTS]"
    output = []
    failed = []

    with open(fpath_geopoints, 'rU') as fin:
        rdr = csv.reader(fin)
        fnames = rdr.next()
        for row in rdr:
            geopoint_dct = collections.OrderedDict(zip(fnames, row))
            loc = extract_geopoint_location(row)

            attribs_dct = loc_to_region_attribs(loc, regions, region_locator, region_attribs)
            if attribs_dct is None:
                failed.append(geopoint_dct)
            else:
                out = collections.OrderedDict()
                out.update(geopoint_dct)
                out.update(attribs_dct)
                output.append(out)

    print "Saving %s rows to %s" % (len(output), fpath_output)
    save_dict_seq(output, fpath_output)

    print "Saving %s rows to %s" % (len(failed), fpath_output_no_region)
    save_dict_seq(failed, fpath_output_no_region)


