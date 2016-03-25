Examples
********

Locations API
=============

Find a Location by Address
--------------------------

Data Fields which you can give for location by address API service:

 - adminDistrict[Optional]: A string that contains a subdivision, such as the abbreviation of a US state
 - locality[Optional]: A string that contains the locality, such as a US city
 - postalCode[Optional]: An integer value that contains the postal code, such as a US ZIP Code
 - addressLine[Optional]: A string specifying the street line of an address
 - countryRegion[Optional]: A string specifying the ISO country code
 - c[Optional]: A string specifying the culture parameter
 - o[Optional]: A string for specifying the format of output(response) Ex. - xml/json
     - If empty, default output would be a JSON data string
     - If given xml, the output would be an xml data string
 - includeNeighborhood[Optional]: One of the following values
     - 1: Include neighborhood information when available
     - 0 [default]: Do not include neighborhood information
 - include[Optional]: The only value for this parameter is ciso2. When you specify include=ciso2, the two-letter ISO country code is included for addresses in the response
     - default='ciso2'
 - maxResults[Optional]: An integer between 1 and 20 (number of results)
     - default=20
 - key[Required]: Bing maps api key
     - Required

The general output format for the location API services can be found at https://msdn.microsoft.com/en-us/library/ff701725.aspx

The below example can help you on how the package helps you to retrieve the data from Location By Address API service (Please check :class:`bingmaps.apiservices.LocationByAddress` for more methods):

.. doctest::

    >>> from bingmaps.apiservices import LocationByAddress
    >>> key = 'Av6_H8GIYQyP-DLQwLOKDknW64QfmVgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'
    >>> data = {'adminDistrict': 'WA',
    ...         'locality': 'Seattle',
    ...         'key': key}
    >>> loc_by_address = LocationByAddress(data)
    >>> print(loc_by_address.status_code)
    200
    >>> print(loc_by_address.get_coordinates)
    [coordinates(latitude=47.60356903076172, longitude=-122.32945251464844)]
    >>> for coord in loc_by_address.get_coordinates:
    ...     print(coord.latitude, coord.longitude)
    47.60356903076172 -122.32945251464844
    >>> print(loc_by_address.get_address)   # doctest: +SKIP
    [{'locality': 'Seattle', 'countryRegionIso2': 'US', 'adminDistrict': 'WA', 'adminDistrict2': 'King Co.', 'formattedAddress': 'Seattle, WA', 'countryRegion': 'United States'}]
    >>> print(loc_by_address.get_bbox)
    [boundingbox(southlatitude=47.253395080566406, westlongitude=-123.16571807861328, northlatitude=47.94615936279297, eastlongitude=-121.5034408569336)]
    >>> for bbox_coord in loc_by_address.get_bbox:
    ...     print(bbox_coord.southlatitude)
    ...     print(bbox_coord.westlongitude)
    ...     print(bbox_coord.northlatitude)
    ...     print(bbox_coord.eastlongitude)
    47.253395080566406
    -123.16571807861328
    47.94615936279297
    -121.5034408569336


Find a Location by Point
------------------------
Data Fields which you can give for location by point API service:

 - point[Required]: A point on the Earth specified by a latitude and longitude.
 - includeEntityTypes[Optional]: A comma separated list of entity types selected from the following options:
    - Address
    - Neighborhood
    - PopulatedPlace
    - Postcode1
    - AdminDivision1
    - AdminDivision2
    - CountryRegion
    These entity types are ordered from the most specific entity to the
    least specific entity. When entities of more than one entity type are
    found, only the most specific entity is returned. For example, if you
    specify Address and AdminDistrict1 as entity types and entities were
    found for both types, only the Address entity information is returned
    in the response. One exception to this rule is when both
    PopulatedPlace and Neighborhood entity types are specified and
    information is found for both. In this case, the information for both
    entity types is returned. Also, more than one Neighborhood may be
    returned because the area covered by two different neighborhoods can
    overlap.
 - includeNeighborhood[Optional]: One of the following values:
    - 1: Include neighborhood information when available.
    - 0 [default]: Do not include neighborhood information.
 - include[Optional]: The only value for this parameter is ciso2. When you specify include=ciso2, the two-letter ISO country code is included
    for addresses in the response.
 - c[Optional]: A string specifying the culture parameter
 - o[Optional]: A string for specifying the format of output(response) Ex. - xml/json
     - If empty, default output would be a JSON data string
     - If given xml, the output would be an xml data string
 - maxResults[Optional]: An integer between 1 and 20 (number of results)
     - default=20
 - key[Required]: Bing maps api key
     - Required

The general output format for the location API services can be found at https://msdn.microsoft.com/en-us/library/ff701725.aspx

The below example can help you on how the package helps you to retrieve the data from Location By Point API service (Please check :class:`bingmaps.apiservices.LocationByPoint` for more methods):

.. doctest::

    >>> from bingmaps.apiservices import LocationByPoint
    >>> key = 'Av6_H8GIYQyP-DLQwLOKDknW64QfmVgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'
    >>> data = {'point': '39.904211,116.407395',
    ...         'includeEntityTypes': 'PopulatedPlace',
    ...         'key': key}
    >>> loc_by_point = LocationByPoint(data)
    >>> print(loc_by_point.status_code)
    200
    >>> print(loc_by_point.get_coordinates)
    [coordinates(latitude=39.91387176513672, longitude=116.37654113769531)]
    >>> for coord in loc_by_point.get_coordinates:
    ...     print(coord.latitude)
    ...     print(coord.longitude)
    39.91387176513672
    116.37654113769531
    >>> print(loc_by_point.get_address)     # doctest: +SKIP
    [{'locality': 'Beijing (Peking)', 'countryRegion': 'China', 'countryRegionIso2': 'CN', 'formattedAddress': 'Beijing (Peking), China'}]
    >>> print(loc_by_point.get_bbox)
    [boundingbox(southlatitude=39.8636474609375, westlongitude=116.27059173583984, northlatitude=39.96409606933594, eastlongitude=116.48249053955078)]
    >>> for bbox_coord in loc_by_point.get_bbox:
    ...     print(bbox_coord.southlatitude)
    ...     print(bbox_coord.westlongitude)
    ...     print(bbox_coord.northlatitude)
    ...     print(bbox_coord.eastlongitude)
    39.8636474609375
    116.27059173583984
    39.96409606933594
    116.48249053955078

Find a Location by Query
------------------------

Data Fields which you can give for location by query API service:

 - q[Required]: A string (query) that contains information about a location, such as an address or landmark name.
 - includeNeighborhood[Optional]: One of the following values:
    - 1: Include neighborhood information when available.
    - 0 [default]: Do not include neighborhood information.
 - include[Optional]: One or more of the following options:
    - queryParse: Specifies that the response shows how the query string
      was parsed into address values, such as addressLine, locality,
      adminDistrict, and postalCode.
    - ciso2: Specifies to include the two-letter ISO country code. If you specify more than one include value, separate the values with a comma.
 - c[Optional]: A string specifying the culture parameter
 - o[Optional]: A string for specifying the format of output(response) Ex. - xml/json
    - If empty, default output would be a JSON data string
    - If given xml, the output would be an xml data string
 - maxResults[Optional]: An integer between 1 and 20 (number of results)
    - default=20
 - key[Required]: Bing maps api key
    - Required

The general output format for the location API services can be found at https://msdn.microsoft.com/en-us/library/ff701725.aspx

The below example can help you on how the package helps you to retrieve the data from Location By Query API service (Please check :class:`bingmaps.apiservices.LocationByQuery` for more methods):

.. doctest::

    >>> from bingmaps.apiservices import LocationByQuery
    >>> key = 'Av6_H8GIYQyP-DLQwLOKDknW64QfmVgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'
    >>> data = {'q': '7266 Canterbury Court Oshkosh, WI 54901',
    ...         'key': key}
    >>> loc_by_query = LocationByQuery(data)
    >>> print(loc_by_query.status_code)
    200
    >>> print(loc_by_query.get_coordinates)
    [coordinates(latitude=44.0088005065918, longitude=-88.57089233398438), coordinates(latitude=44.26647186279297, longitude=-88.36396789550781), coordinates(latitude=44.268680572509766, longitude=-88.36396026611328)]
    >>> for coord in loc_by_query.get_coordinates:
    ...     print(coord.latitude)
    ...     print(coord.longitude)
    44.0088005065918
    -88.57089233398438
    44.26647186279297
    -88.36396789550781
    44.268680572509766
    -88.36396026611328
    >>> print(loc_by_query.get_address)     # doctest: +SKIP
    [{'countryRegion': 'United States', 'adminDistrict': 'WI', 'postalCode': '54902', 'addressLine': 'Canterbury Dr', 'formattedAddress': 'Canterbury Dr, Oshkosh, WI 54902', 'adminDistrict2': 'Winnebago Co.', 'locality': 'Oshkosh', 'countryRegionIso2': 'US'}, {'countryRegion': 'United States', 'adminDistrict': 'WI', 'postalCode': '54915', 'addressLine': 'Canterbury Ct', 'formattedAddress': 'Canterbury Ct, Appleton, WI 54915', 'adminDistrict2': 'Outagamie Co.', 'locality': 'Appleton', 'countryRegionIso2': 'US'}, {'countryRegion': 'United States', 'adminDistrict': 'WI', 'postalCode': '54915', 'addressLine': 'N Canterbury Dr', 'formattedAddress': 'N Canterbury Dr, Appleton, WI 54915', 'adminDistrict2': 'Outagamie Co.', 'locality': 'Appleton', 'countryRegionIso2': 'US'}]
    >>> print(loc_by_query.get_bbox)
    [boundingbox(southlatitude=44.00493778902112, westlongitude=-88.57805267570657, northlatitude=44.01266322416247, eastlongitude=-88.56373199226218), boundingbox(southlatitude=44.26260914522229, westlongitude=-88.3711595479266, northlatitude=44.270334580363645, eastlongitude=-88.35677624308903), boundingbox(southlatitude=44.26481785493909, westlongitude=-88.37115218873478, northlatitude=44.27254329008044, eastlongitude=-88.35676834349178)]


Elevations API
==============

There are 4 methods in elevations API services: List/Polyline/SeaLevel/Bounds

Elevations for latitude and longitude coordinates
-------------------------------------------------

Data Fields which you can give for getting elevations for latitude and longitude coordinates:

 - method[Required]: A method for calculating elevations (ex. List/Polyline/SeaLevel/Bounds)
   - 'List' [default]: Use this for returning elevations for a given pair of coordinates.
 - points[Required]:  A set of coordinates on the Earth to use in
   elevation calculations. The exact use of these points depends on the
   type of elevation request. A set of latitude and longitude values in
   WGS84 decimal degrees. If you are requesting elevations or elevation
   offsets for a set of points, the maximum number of points is 1024.
   Points should be given as ``lat1,long1,lat2,long2,latn,longn``
 - heights[Optional]: A string that specifies which sea level model to use to calculate elevation. One of the following values:
   - sealevel [default]: Use the geoid Earth model (EGM2008 2.5’).
   - ellipsoid: Use the ellipsoid Earth model (WGS84).
 - o[Optional]: A string specifying the output as JSON or xml.
 - key[Required]: Bing maps key

The general output format for the elvations API services can be found at https://msdn.microsoft.com/en-us/library/hh441730.aspx

The below example can help you on how the package helps you to retrieve elevations from latitudes and longitude coordinates (Please check :class:`bingmaps.apiservices.ElevationsApi` for more methods):

.. doctest::

   >>> from bingmaps.apiservices import ElevationsApi
   >>> key = 'Av6_H8GIYQyP-DLQwLOKDknW64QfmVgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'
   >>> data = {'method': 'List',
   ...         'points': [15.5467, 34.5676],
   ...         'key': key}
   >>> elevations = ElevationsApi(data)
   >>> print(elevations.status_code)
   200
   >>> print(elevations.elevations)
   [elevations_data(elevations=[471])]
   >>> for elevation in elevations.elevations:
   ...     print(elevation.elevations)
   [471]
   >>> print(elevations.zoomlevel)
   [zoomlevel(zoomLevel=11)]
   >>> for zlevel in elevations.zoomlevel:
   ...     print(zlevel.zoomLevel)
   11

Elevations at equally-spaced locations along a polyline path
------------------------------------------------------------

Data Fields which you can give for getting Elevations at equally-spaced locations along a polyline path:

 - method[Required]: A method for calculating elevations (ex. List/Polyline/SeaLevel/Bounds)
   - 'Polyline' [default]: Use this for returning elevations for a given pair of coordinates.
 - points[Required]:  A set of coordinates on the Earth to use in
   elevation calculations. The exact use of these points depends on the
   type of elevation request. A set of latitude and longitude values in
   WGS84 decimal degrees. If you are requesting elevations or elevation
   offsets for a set of points, the maximum number of points is 1024.
   Points should be at least 2 pairs of latitudes and longitudes for
   Polyline method - It should be a minimum total of 4 points for
   Polyline method. Points should be given as
   ``lat1,long1,lat2,long2,latn,longn``
 - heights[Optional]: A string that specifies which sea level model to use to calculate elevation. One of the following values:
   - sealevel [default]: Use the geoid Earth model (EGM2008 2.5’).
   - ellipsoid: Use the ellipsoid Earth model (WGS84).
 - samples[Required]: Specifies the number of equally-spaced elevation
   values to provide along a polyline path. A positive integer. The
   maximum number of samples is 1024.
 - o[Optional]: A string specifying the output as JSON or xml.
 - key[Required]: Bing maps key

The general output format for the elvations API services can be found at https://msdn.microsoft.com/en-us/library/hh441730.aspx

The below example can help you on how the package helps you to retrieve elevations at equally-spaced locations along a polyline path (Please check :class:`bingmaps.apiservices.ElevationsApi` for more methods):

.. doctest::

   >>> from bingmaps.apiservices import ElevationsApi
   >>> key = 'Av6_H8GIYQyP-DLQwLOKDknW64QfmVgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'
   >>> data = {'method': 'Polyline',
   ...         'points': [35.89431, -110.72522, 35.89393, -110.72578],
   ...         'samples': 10,
   ...         'key': key}
   >>> elevations = ElevationsApi(data)
   >>> print(elevations.status_code)
   200
   >>> print(elevations.elevations)
   [elevations_data(elevations=[1776, 1775, 1775, 1775, 1775, 1775, 1775, 1775, 1775, 1775])]
   >>> for elevation in elevations.elevations:
   ...     print(elevation.elevations)
   [1776, 1775, 1775, 1775, 1775, 1775, 1775, 1775, 1775, 1775]
   >>> print(elevations.zoomlevel)
   [zoomlevel(zoomLevel=14)]

Get offset at a set of latitude and longitude coordinates
---------------------------------------------------------

Data Fields which you can give for getting offset at a set of latitude and longitude coordinates:

 - method[Required]: A method for calculating elevations (ex. List/Polyline/SeaLevel/Bounds)
   - 'SeaLevel' [default]: Use this for returning elevations for a given pair of coordinates.
 - points[Required]:  A set of coordinates on the Earth to use in
   elevation calculations. The exact use of these points depends on the
   type of elevation request. A set of latitude and longitude values in
   WGS84 decimal degrees. If you are requesting elevations or elevation
   offsets for a set of points, the maximum number of points is 1024.
   Points should be given as ``lat1,long1,lat2,long2,latn,longn``
 - o[Optional]: A string specifying the output as JSON or xml.
 - key[Required: Bing maps key

The general output format for the elvations API services can be found at https://msdn.microsoft.com/en-us/library/hh441730.aspx

The below example can help you on how the package helps you to retrieve elevations at a set of latitude and longitude coordinates (Please check :class:`bingmaps.apiservices.ElevationsApi` for more methods):

.. doctest::

   >>> from bingmaps.apiservices import ElevationsApi
   >>> key = 'Av6_H8GIYQyP-DLQwLOKDknW64QfmVgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'
   >>> data = {'method': 'SeaLevel',
   ...         'points': [15.5467, 34.5676],
   ...         'key': key}
   >>> elevations = ElevationsApi(data)
   >>> print(elevations.status_code)
   200
   >>> print(elevations.elevations)
   [elevations_data(elevations=[0])]
   >>> print(elevations.zoomlevel)
   [zoomlevel(zoomLevel=14)]

Get elevations within an area on the Earth defined as a bounding box
--------------------------------------------------------------------

Data Fields which you can give for getting elevations within an area on the Earth defined as a bounding box:

 - method[Required]: A method for calculating elevations (ex. List/Polyline/SeaLevel/Bounds)
   - 'Bounds' [default]: Use this for returning elevations for a given pair of coordinates.
 - bounds[Required]: Specifies the rectangular area over which to
   provide elevation values. A bounding box defined as a set of WGS84
   latitudes and longitudes in the following order:
   - south latitude, west longitude, north latitude, east longitude
   - REQUIRED field
 - rows,cols[Required]: Specifies the number of rows and columns to use
   to divide the bounding box area into a grid. The rows and columns that
   define the bounding box each count as two (2) of the rows and columns.
   Elevation values are returned for all vertices of the grid. Integers
   with a value of two (2) or greater. The number of rows and columns
   can define a maximum of 1024 locations (rows * cols <= 1024).
 - heights[Optional]: A string that specifies which sea level model to
   use to calculate elevation. One of the following values:
   - sealevel [default]: Use the geoid Earth model (EGM2008 2.5’).
   - ellipsoid: Use the ellipsoid Earth model (WGS84).
 - o[Optional]: A string specifying the output as JSON or xml.
 - key[Required]: Bing maps key

The general output format for the elvations API services can be found at https://msdn.microsoft.com/en-us/library/hh441730.aspx

The below example can help you on how the package helps you to retrieve elevations within an area on the Earth defined as a bounding box (Please check :class:`bingmaps.apiservices.ElevationsApi` for more methods):

.. doctest::

   >>> from bingmaps.apiservices import ElevationsApi
   >>> key = 'Av6_H8GIYQyP-DLQwLOKDknW64QfmVgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'
   >>> data = {'method': 'Bounds',
   ...         'bounds': [15.5463, 34.6577, 16.4365, 35.3245],
   ...         'rows': 4,
   ...         'cols': 5,
   ...         'key': key}
   >>> elevations = ElevationsApi(data)
   >>> print(elevations.status_code)
   200
   >>> print(elevations.elevations)
   [elevations_data(elevations=[482, 467, 464, 457, 452, 432, 419, 418, 422, 419, 394, 394, 399, 403, 409, 386, 387, 397, 396, 401])]
   >>> print(elevations.zoomlevel)
   [zoomlevel(zoomLevel=9)]

Traffic Incidents API
=====================

Data Fields which you can give for Traffic Incidents API service:

 - mapArea[Required]: A rectangular area specified as a bounding box. The size of the area can be a maximum of 500 km x 500 km. A bounding
    box defines an area by specifying SouthLatitude, WestLongitude,
    NorthLatitude, and EastLongitude values.
 - includeLocationCodes[Optional]:  One of the following values:
    - 'true'
    - 'false' [default]
    If you want to use the default value, you can omit this parameter from
    the URL request.
 - severity[Optional]: One or more of the following integer values:
    - 1: LowImpact
    - 2: Minor
    - 3: Moderate
    - 4: Serious
    The default is to return traffic incidents for all severity levels.
 - type[Optional]: One or more of the following integer values:
    - 1: Accident
    - 2: Congestion
    - 3: DisabledVehicle
    - 4: MassTransit
    - 5: Miscellaneous
    - 6: OtherNews
    - 7: PlannedEvent
    - 8: RoadHazard
    - 9: Construction
    - 10: Alert
    - 11: Weather
 - o[Optional]: A string specifying the output as JSON or xml.
 - key[Required]: Bing maps key - REQUIRED field

The general output format for the Traffic Incidents API services can be found at https://msdn.microsoft.com/en-us/library/hh441730.aspx

The below example can help you on how the package helps you to retrieve the data from Traffic Incidents API service (Please check :class:`bingmaps.apiservices.TrafficIncidentsApi` for more methods):

.. doctest::

    >>> from bingmaps.apiservices import TrafficIncidentsApi
    >>> key = 'Av6_H8GIYQyP-DLQwLOKDknW64QfmVgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'
    >>> data = {'mapArea': [37, -105, 45, -94],
    ...         'includeLocationCodes': 'true',
    ...         'severity': [3],
    ...         'key': key}
    >>> incidents = TrafficIncidentsApi(data)
    >>> print(incidents.status_code)
    200
    >>> print(incidents.congestion)
    None
    >>> print(incidents.description)    # doctest: +SKIP
    [description(description='Between Floyd Blvd/Exit 147A and I-129/US-75/US-20/Exit 144 - Construction work.'), description(description='At I-29 - Construction work. Lane closed.'), description(description='Between I-29 and Louise Ave/Exit 1 - Construction work.'), description(description='Between US-75/Industrial Road/Exit 143 and Floyd Blvd/Exit 147A - Construction work. Lane closed. Contraflow.'), description(description='At I-29 - Construction work. Lane closed.')]
    >>> print(incidents.detour_info)
    None
    >>> print(incidents.incident_id)    # doctest: +SKIP
    [incident_id(incident_id=499108686961573047), incident_id(incident_id=4181860463540379194), incident_id(incident_id=163095513463170197), incident_id(incident_id=990321114056185509), incident_id(incident_id=1250781520351805422)]
    >>> print(incidents.incident_id[0].incident_id)     # doctest: +SKIP
    499108686961573047
    >>> print(incidents.get_coordinates)    # doctest: +SKIP
    [coordinates(latitude=42.48766, longitude=-96.39704), coordinates(latitude=41.220444, longitude=-95.832393), coordinates(latitude=43.49234, longitude=-96.78513), coordinates(latitude=42.44252, longitude=-96.3752), coordinates(latitude=41.21952, longitude=-95.83334)]
    >>> print(incidents.get_coordinates[0].latitude, incidents.get_coordinates[0].longitude)    # doctest: +SKIP
    42.48766 -96.39704
    >>> print(incidents.lane_info)
    None
    >>> print(incidents.start_time)     # doctest: +SKIP
    [start_time(start_time='/Date(1458053489000)/'), start_time(start_time='/Date(1458053489000)/'), start_time(start_time='/Date(1458053489000)/'), start_time(start_time='/Date(1458053489000)/'), start_time(start_time='/Date(1458053489000)/')]
    >>> print(incidents.end_time)   # doctest: +SKIP
    [end_time(end_time='/Date(1458870690000)/'), end_time(end_time='/Date(1481644800000)/'), end_time(end_time='/Date(1458939600000)/'), end_time(end_time='/Date(1481644800000)/'), end_time(end_time='/Date(1458870690000)/')]
    >>> print(incidents.is_verified)    # doctest: +SKIP
    [verified(verified=True), verified(verified=True), verified(verified=True), verified(verified=True), verified(verified=True)]
    >>> print(incidents.last_modified)  # doctest: +SKIP
    last_modified(last_modified='/Date(1458866786528)/'), last_modified(last_modified='/Date(1458866693135)/'), last_modified(last_modified='/Date(1458866786528)/')]
    >>> print(incidents.severity)   # doctest: +SKIP
    [severity(severity=3), severity(severity=3), severity(severity=3), severity(severity=3), severity(severity=3)]
    >>> print(incidents.type)   # doctest: +SKIP
    [type(type=9), type(type=9), type(type=9), type(type=9), type(type=9)]

.. note::
   Most of the outputs above are list of named tuples.

