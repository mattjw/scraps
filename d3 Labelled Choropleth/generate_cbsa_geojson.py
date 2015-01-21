# Matt J Williams, 2015
# http://mattjw.net
# mattjw@mattjw.net


import re
import json
from collections import OrderedDict

import unicodecsv
import shapefile
import shapely.geometry


def region_shape_generator(shape_base_fname):
        """
        Yields dictionaries. Each dictionary has:
            'pyshp'    the geometry directly from pyshp
            'shapely'  a shapely MultiPolygon, which has been
                       obtained by converting from the pyshp representation
        ...and the fields from the shapefile record.
        """
        sf = shapefile.Reader(shape_base_fname)
        fields = sf.fields[1:]

        gIter = sf.iterShapes()
        rIter = sf.iterRecords()

        while True:
            try:
                shp = gIter.next()
                rec = rIter.next()

                dct = OrderedDict()  # combined data

                #
                # pyshp geometry
                dct['pyshp'] = shp

                #
                # convert to shapely object
                assert shp.shapeType == 5
                    # 5 => shapefile's "Polygon" type, which may have multiple 'parts':
                    #     fields = MBR, Number of parts, Number of points, Parts, Points
                    # i.e., a shapefil Polygon may actually include multiple polygons
                    # shp.parts: this is a list of indexes, indicating the start of
                    # a new shape

                num_parts = len(shp.parts)
                num_points = len(shp.points)
                polys = []
                for i in xrange(num_parts):
                    start_indx = shp.parts[i]
                    if (i+1) < num_parts:
                        end_indx = shp.parts[i+1]
                    else:
                        end_indx = num_points
                    poly_pts = shp.points[start_indx:end_indx]
                    poly = shapely.geometry.Polygon(poly_pts)
                    polys.append(poly)
                mpoly = shapely.geometry.MultiPolygon(polygons=polys)  # assume no holes
                assert sum(len(poly.exterior.coords) for poly in polys) == num_points  # check the points for individual polys sums to total points

                dct['shapely'] = mpoly

                #
                # Finally, the records...

                for indx, fieldtup in enumerate(fields):
                    field = fieldtup[0]
                    dct[field] = rec[indx]

                yield dct
            except StopIteration:
                break


if __name__ == "__main__":
    #
    # Args
    fpath_region_stats_orig = "./dat/region_statistics.csv"
    fpath_cbsa_shapes = "./dat/cb_2013_us_cbsa_500k"

    fpath_out_region_stats_abbrevs = "./dat/region_statistics_abbrevs.csv"
    fpath_out_regions_geojson = "./dat/regions_geojson.json"

    variate = 'users'  # value to plot on choropleth

    #
    # Read
    rows = tuple(unicodecsv.DictReader(open(fpath_region_stats_orig)))

    #
    # Region abbrevs
    for row in rows:
        name = row['region']
        name = name.split(',')[0]
        name = re.sub(r"[a-z \.]", '', name)
        row['region_abbr'] = name

    assert len(set(row['region_abbr'] for row in rows)) == len(rows), "region abbrevs are not unique"

    fout = open(fpath_out_region_stats_abbrevs, 'w')
    cols = rows[0].keys()
    wrtr = unicodecsv.DictWriter(fout, cols)
    wrtr.writeheader()
    wrtr.writerows(rows)
    fout.close()

    # 
    # Build geoms (geoJSON in Python) for chosen cities, and combine with
    # chosen variate
    viz_regions = {}  # dict of regions to visualise. 
                      # dict of dicts.
                      # key = region fullname.
                      # val = {geom, abbr, value}
    for row in rows:
        d = OrderedDict()
        d['geojson'] = None
        d['abbr'] = row['region_abbr']
        d['val'] = row[variate]

        fullname = row['region']
        
        viz_regions[fullname] = d

    for region_dct in region_shape_generator(fpath_cbsa_shapes):
        region_label = region_dct['NAME']  # region fullname
        if region_label in viz_regions:
            multi_poly = region_dct['shapely']
            geojson = shapely.geometry.mapping(multi_poly)
            viz_regions[region_label]['geojson'] = geojson


    assert all(r['geojson'] is not None for r in viz_regions.itervalues())

    # combine into valid geojson collection format
    geojson_collection = {}
    geojson_collection['type'] = 'FeatureCollection'
    geojson_collection['features'] = []
    indx = 1
    for region_fullname, dct in viz_regions.iteritems():
        item = {'type': 'Feature', 'id': indx, 'properties': {}}
        item['properties']['name_full'] = region_fullname
        item['properties']['name_cities'] = region_fullname.split(',')[0]
        item['properties']['name_abbr'] = dct['abbr']
        item['properties']['value'] = dct['val']
        item['geometry'] = dct['geojson']
        geojson_collection['features'].append(item)
        indx += 1

    fout = open(fpath_out_regions_geojson, 'w')
    json.dump(geojson_collection, fout)
    fout.close()
