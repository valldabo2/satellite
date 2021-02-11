# satellite

Project to download satellite data, annotate it, and make model predictions. Especially for forest fires.

## Data

European satellite data is available via python client sentinelsat.

Information about api here: https://sentinelsat.readthedocs.io/en/stable/ 

- One year historical data (older can be requested)
- 5 days update frequency
- Sentinel-2 gives visual light (forest fires)
- Sentinel-5 gives other wavelengths (methane detection)

### Forest fires
Californian forest fires can be found at: https://www.fire.ca.gov/incidents/2020/

To get a geomap.json for a certain area: https://geojson.io/#map=2/20.0/0.0

To view Sentinel 2 data: [link](https://apps.sentinel-hub.com/sentinel-playground/?source=S2L2A&lat=38.6989521545997&lng=-122.76308119297028&zoom=11&preset=6_SWIR&layers=B01,B02,B03&maxcc=100&gain=1.0&gamma=1.0&time=2019-04-01%7C2019-10-27&atmFilter=&showDates=truehttps://apps.sentinel-hub.com/sentinel-playground/?source=S2&lat=31.77546135026095&lng=5.611610412597656&zoom=4&preset=1-NATURAL-COLOR&layers=B01,B02,B03&maxcc=100&gain=1.0&gamma=1.0&time=2020-08-01%7C2021-02-11&atmFilter=&showDates=false)

### Forest fire cases

#### Glass-fire
[Incident](https://www.fire.ca.gov/incidents/2020/9/27/glass-fire/)
[View data](https://apps.sentinel-hub.com/sentinel-playground/?source=S2L2A&lat=38.54986874686269&lng=-122.56942838430405&zoom=11&preset=6_SWIR&layers=B01,B02,B03&maxcc=100&gain=1.0&gamma=1.0&time=2020-03-01%7C2020-09-29&atmFilter=&showDates=true)
[Geojson](http://geojson.io/#map=10/38.5546/-122.5573)

### Methane leaks
Resources:
- https://www.reuters.com/article/us-climatechange-methane-satellites-insi-idUSKBN23W3K4
- https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-5P/Methane_and_ozone_data_products_from_Copernicus_Sentinel-5P
- https://www.delta.tudelft.nl/article/finding-methane-leaks
- https://www.esa.int/ESA_Multimedia/Images/2019/12/Methane_leak_visible_from_space
- https://earthobservatory.nasa.gov/images/88245/imaging-a-methane-leak-from-space

# Todos

[ ] Write download script for multiple forest fire cases
[ ] Inspect downloaded data
[ ] Find annotation program and annotate data
[ ] Find appropriate model for detection, object detection, prediction of forest fires
[ ] Synthesize with weather data
[ ] How to identify methane gas leaks?
[ ] Get known cases of forest fires
[ ] Get known cases of methane leaks
