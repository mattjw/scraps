# Matt J Williams, 2015
# http://mattjw.net
# mattjw@mattjw.net


from shapefile_tools import polygon_shaperecords


if __name__ == "__main__":
    fpath_cbsa_shapefile_base = "./dat/cb_2013_us_cbsa_500k"
    min_polys = 8

    print
    print "List of CBSAs that are composed of %s or more polygons" % (min_polys)
    print
    
    fmt = "%-50s  %-20s"
    print fmt % ('CBSA name', 'Num. Polygons')
    print

    for shape_dict in polygon_shaperecords(fpath_cbsa_shapefile_base):
        cbsa_name = shape_dict['NAME']
        geom = shape_dict['geom_shapely']
        num_polys = len(geom.geoms)

        if num_polys >= min_polys:
            print fmt % (cbsa_name, num_polys)
