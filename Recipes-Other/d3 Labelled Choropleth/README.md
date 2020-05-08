Build a choropleth visualisation using d3, a complete example. Includes full data processing pipeline in Python. The resulting visualisation maps US states, US core-based statistical areas (CBSAs), and the number of Foursquare users in each CBSA.

### Data pipeline

Inputs (see `dat` directory):

* `cb_2013_us_cbsa_500k.*`: Cartographic Boundary Shapefiles - Metropolitan and Micropolitan Statistical Areas and Related Statistical Areas. https://www.census.gov/geo/maps-data/data/cbf/cbf_msa.html
* `region_statistics.csv`: statistics concerning a subset of CBSAs.
* `us-states.json`: Polygons for US states, plus other properties for each state. GeoJSON format.

Processing:

* Run `generate_cbsa_geojson.py`. This will generate the CSV including abbreviations (`region_statistics_abbrevs.csv`) and GeoJSON data (`regions_geojson.json`).
* The generated GeoJSON appears to be buggy, or at least cannot be directly loaded in d3. Instead, we process it with mapshaper ()`http://www.mapshaper.org/`) and export it to a GeoJSON file. Save as a JSON file named `regions_geojson__mapshaped.json`.
* Run visualisation in D3. See: `choro_viz_d3*.html`.

Can be opened on local browser, if browser permits JavaScript loading files via the `file://` scheme. Firefox allows this by default. In Chrome on OS X, launch with the relevant flag:

```
$ "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --allow-file-access-from-files
```

### Example d3 files

`choropleth_CBSA_vertleg.html`: Vertical legend. Equi-rectangular projection.

`choropleth_CBSA_horizleg.html`: Horizontal legend. Conformal conic projection (similar appearance to Mercator). Other improvements to apperance.


### Saving SVG as PDF

* Open in browser.
* Print and save as PDF.
* Crop whitespace using the `pdfcrop` CL-tool. (Bundled with most latex distros.)

### Useful references for d3, GeoJSON, and TopoJSON

`http://bl.ocks.org/mbostock/raw/4207744/`
swiss cantons using topo json. including text labels. full working example.

`http://synthesis.sbecker.net/articles/2012/07/18/learning-d3-part-7-choropleth-maps`
choropleth for us states. and blues colouring. quantization. geojson.

`http://bl.ocks.org/mbostock/4060606`
topojson equivalent of above.

d3 beginners guides:
`http://www.d3noob.org/2013/03/a-simple-d3js-map-explained.html`
`http://www.jeromecukier.net/blog/2012/09/04/getting-to-hello-world-with-d3/`

long GeoJSON guide:
`http://chimera.labs.oreilly.com/books/1230000000345/ch12.html#_json_meet_geojson`



