## Shapefile Reading

### `shapefile_tools.py`

Function `polygon_shaperecords` handles combining shapefile shapes with their records (list of attributes). It acts as a generator that yields dictionaries. Each dictionary combines the shape and records for a particular shape.

### `demo.py`

A demonstration of the shapefile loader. Uses US Ceneus CBSA (multi-)polygons.

### Why?

`shapely` and `pyshp` are two useful Python packages for managing shapes and their geometry (`shapely`) and shapefiles (`pyshp`). `pyshp` is good at loading shapefile data, but `shapely` shapes are much more useful for processing and manipulating geometry. Unfortunately, converting between the two takes a bit of work.  Also, `pyshp` does not provide a /combined/ way of loading shape records along with their geometry.

This code solves these two problems. It combines shapefile shape geometry and records into a dictionary, and also builds a `shapely` object for the corresponding (multi-)polygon.

See ``shapefile_tools.py` for usage.


## Annotating geopoints

Scenario: You have a CSV file where each row represents a geographic point, with some additional information on that location. For example, this might be a CSV file of Foursquare venues, including their venue name, ID, and longitude and latitude. You want to extend this CSV with some additional information about the region (ward, city, state, constituency, etc.) that each geopoint belongs to. E.g., annotate each Foursquare venue with some demographic information about the electoral ward it belongs to.

This is implemented by `annotate_geopoints.py`.