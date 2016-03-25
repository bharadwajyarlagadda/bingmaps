from marshmallow import fields, Schema, post_dump, validate


class ElevationsUrl(object):
    """This class helps in building a url for elevations API service.

    :ivar data: Data required for building up the URL
    :ivar protocol: http protocol for the url
    :ivar schema: Elevations schema to which the data will be dumped

    All the URL values are retrieved from the schema.

    Example:

        ::

            >>> data = {'method': 'Polyline',
            ...         'points': [35.89431,
            ...                    -110.72522,
            ...                    35.89393,
            ...                    -110.72578],
            ...         'samples': 10,
            ...         'key': 'abs'}
            >>> url = ElevationsUrl(data, 'http', Polyline())
            >>> url.main_url
            'dev.virtualearth.net'
            >>> url.protocol
            'http:/'
            >>> url.resourcePath

            >>> url.restApi
            'Elevation'
            >>> url.rest
            'REST'
            >>> url.version
            'v1'
            >>> url.query
            'Polyline?points=35.89431,-110.72522,35.89393,-110.72578&h\
eights=sealevel&samples=10&key=abs'
    """
    def __init__(self, data, protocol, schema):
        self.data = data
        self.http_protocol = protocol
        self.schema_dict = self.schema_values(schema)

    def schema_values(self, schema):
        is_valid_schema = schema.validate(self.data)
        if bool(is_valid_schema):
            raise KeyError(is_valid_schema)
        else:
            return schema.dump(self.data).data

    @property
    def protocol(self):
        """This property helps in returning the http protocol to be used as
        part of the URL.

        :ivar http_protocol: The http protocol passed in (http/https)

        :getter: Returns a string relevant to the http
            protocol
              - http: ``http:/``
              - https: ``https:/``
        :type: string
        """
        if self.http_protocol == 'http':
            return 'http:/'
        else:
            return 'https:/'

    @property
    def main_url(self):
        """This property helps in returning the main URL used in bingmaps rest
        services

        :getter: Returns a
            URL
              - ``dev.virtualearth.net``
        :type: string
        """
        return 'dev.virtualearth.net'

    @property
    def rest(self):
        """This property make the URL accessible for REST services.

        :getter: Returns a string saying that the URL is a REST service
            URL
              - ``REST``
        :type: string
        """
        return 'REST'

    @property
    def version(self):
        """This property gives the version of the Bing Maps REST services

        :getter: Returns a string of Bing Maps REST services
            version
              - ``v1`` for Elevations services
        :type: string
        """
        if 'version' in self.schema_dict:
            return self.schema_dict['version']
        else:
            return None

    @property
    def restApi(self):
        """This property gives a part of the URL that identifies the REST API

        :getter: Returns a part of the URL that identifies the REST
            API
              - ``Elevations`` for Elevations services
        :type: string
        """
        if 'restApi' in self.schema_dict:
            return self.schema_dict['restApi']
        else:
            return None

    @property
    def resourcePath(self):
        """This property gives a part of the URL that specifies a resource
        such as an address or landmark.

        :getter: Returns a string that identifies the resource path such as
            address or landmark
              - ``None`` for Elevations services
        :type: string
        """
        if 'resourcePath' in self.schema_dict:
            return self.schema_dict['resourcePath']
        else:
            return None

    @property
    def query(self):
        """This property helps in retrieving the query part of the URL

        :getter: Returns a part of the URL which consist of all the query
            parameters.
        :type: string
        """
        return self.schema_dict['query']


class Elevations(Schema):
    """Main class for Elevations API schema

    Data Fields:

    :ivar version: A string containing v and an integer that specifies
        the version of the Bing Maps REST Services.
          - default: v1
    :ivar restApi: A part of the URL path that identifies the REST
        API.
          - default: 'Elevation' (for Elevations API services)
    :ivar resourcePath: A part of the URL path that specifies a
        resource, such as an address or landmark.

    This schema helps in creating the main parameters of all types of
    elevations API based services (List, Polyline, SeaLevel, Bounds). The
    above mentioned data fields make up the main parameters of the
    url.

    Example:
        The below example can show you a typical example for how the main URL
        parameters can be passed in as a dictionary
        ::

            >>> data = {'version': 'v1',
            ...         'restApi': 'Elevation',
            ...         'resourcePath': ''}

        When you dump an empty dictionary, the class helps you in filling the
        dictionary with default values. You can see the same behaviour in the
        below example:

        ::

            >>> data = {}
            >>> schema = Elevations()
            >>> schema.dump(data).data
            OrderedDict([('version', 'v1'), ('restApi', 'Elevation')])

    .. note:: Elevations class is common for all the elevations based services
        with the same default data.
    """
    version = fields.Constant(
        'v1'
    )
    restApi = fields.Constant(
        'Elevation'
    )
    resourcePath = fields.Str()

    class Meta:
        """Meta class helps in ordering all the fields in the specified order
        """
        fields = ('version', 'restApi', 'resourcePath')
        ordered = True


class Coordinates(Elevations, Schema):
    """Inherited from :class:`Elevations`

    Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Data Fields for the schema (taken from
    https://msdn.microsoft.com/en-us/library/jj158961.aspx):

    :ivar method[Required]: A method for calculating elevations
        (ex. List/Polyline/SeaLevel/Bounds) - REQUIRED field
          - 'List' [default]: Use this for returning elevations for a given
            pair of coordinates.
    :ivar points[Required]:  A set of coordinates on the Earth to use in
        elevation calculations. The exact use of these points depends on the
        type of elevation request. A set of latitude and longitude values in
        WGS84 decimal degrees. If you are requesting elevations or elevation
        offsets for a set of points, the maximum number of points is 1024.
        Points should be given as ``lat1,long1,lat2,long2,latn,longn`` -
        REQUIRED field
    :ivar heights[Optional]: A string that specifies which sea level model to
        use to calculate elevation. One of the following values:
          - sealevel [default]: Use the geoid Earth model (EGM2008 2.5’).
          - ellipsoid: Use the ellipsoid Earth model (WGS84).
    :ivar o[Optional]: A string specifying the output as JSON or xml.
    :ivar key[Required]: Bing maps key - REQUIRED field

    This schema helps in serializing the data.

    Post-Dump:
        After dumping the data, build_query_string builds up the
        queryParameters string. The final value after dumping the data would
        be a string.

    Example:

        ::

            >>> data = {'method': 'List',
            ...         'points': [15.5467, 34.5676],
            ...         'key': 'abs'}
            >>> schema = Coordinates()
            >>> schema.dump(data).data
            OrderedDict([('version', 'v1'), ('restApi', 'Elevation'), ('query\
', 'List?points=15.5467,34.5676&heights=sealevel&key=abs')])
    """
    method = fields.Str(
        required=True,
        validate=validate.Equal(
            'List',
            error='The method should be List'
        ),
        error_messages={'required': 'method for calculating elevations should'
                                    'be specified'}
    )
    points = fields.List(
        fields.Float,
        validate=validate.Length(
            min=2,
            error='Both latitude and longitude should be entered'
        ),
        required=True,
        error_messages={'required': 'Latitudes, Longitudes not specified'}
    )
    heights = fields.Str(
        default='sealevel'
    )
    o = fields.Str()
    key = fields.Str(
        required=True,
        error_messages={'required': 'Need Bing maps key'}
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'method', 'points',
                  'heights', 'o', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        """This method occurs after dumping the data into the class.

        Args:
            data (dict): dictionary of all the query values

        Returns:
            data (dict): ordered dict of all the values
        """
        query = []
        keys_to_be_removed = []
        for key, value in data.items():
            if key not in ['version', 'restApi', 'resourcePath']:
                if not key == 'method':
                    if key == 'points':
                        value = ','.join(str(val) for val in value)
                        keys_to_be_removed.append(key)
                    query.append('{0}={1}'.format(key, value))
                    keys_to_be_removed.append(key)
                keys_to_be_removed.append(key)
        querystring = '&'.join(query)
        data['query'] = '{0}?{1}'.format(data['method'], querystring)
        for k in list(set(keys_to_be_removed)):
            del data[k]
        return data


class Polyline(Elevations, Schema):
    """Inherited from :class:`Elevations`

    Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Data Fields for the schema (taken from
    https://msdn.microsoft.com/en-us/library/jj158961.aspx):

    :ivar method[Required]: A method for calculating elevations
        (ex. List/Polyline/SeaLevel/Bounds) - REQUIRED field
          - 'Polyline' [default]: Use this for returning elevations for a
            given pair of coordinates.
    :ivar points[Required]:  A set of coordinates on the Earth to use in
        elevation calculations. The exact use of these points depends on the
        type of elevation request. A set of latitude and longitude values in
        WGS84 decimal degrees. If you are requesting elevations or elevation
        offsets for a set of points, the maximum number of points is 1024.
        Points should be at least 2 pairs of latitudes and longitudes for
        Polyline method - It should be a minimum total of 4 points for
        Polyline method. Points should be given as
        ``lat1,long1,lat2,long2,latn,longn``
    :ivar heights[Optional]: A string that specifies which sea level model to
        use to calculate elevation. One of the following values:
          - sealevel [default]: Use the geoid Earth model (EGM2008 2.5’).
          - ellipsoid: Use the ellipsoid Earth model (WGS84).
    :ivar samples[Required]: Specifies the number of equally-spaced elevation
        values to provide along a polyline path. A positive integer. The
        maximum number of samples is 1024.
    :ivar o[Optional]: A string specifying the output as JSON or xml.
    :ivar key[Required]: Bing maps key - REQUIRED field

    This schema helps in serializing the data.

    Post-Dump:
        After dumping the data, build_query_string builds up the
        queryParameters string. The final value after dumping the data would
        be a string.

    Example:

        ::

            >>> data = {'method': 'Polyline',
            ...         'points': [35.89431, -110.72522, 35.89393, -110.72578],
            ...         'samples': 10,
            ...         'key': 'abs'}
            >>> schema = Polyline()
            >>> schema.dump(data).data
            OrderedDict([('version', 'v1'), ('restApi', 'Elevation'), ('query\
', 'Polyline?points=35.89431,-110.72522,35.89393,-110.72578&heights=sealevel&\
samples=10&key=abs')])
    """
    method = fields.Str(
        required=True,
        validate=validate.Equal(
            'Polyline',
            error='The method should be Polyline'
        ),
        error_messages={'required': 'method for calculating elevations should'
                                    'be specified'}
    )
    points = fields.List(
        fields.Float,
        validate=validate.Length(
            min=4,
            error='At least 2 locations should be provided'
        ),
        required=True,
        error_messages={'required': 'Latitudes, Longitudes not specified'}
    )
    heights = fields.Str(
        default='sealevel'
    )
    samples = fields.Int(
        required=True,
        error_messages={'required': 'need a samples value'}
    )
    o = fields.Str()
    key = fields.Str(
        required=True,
        error_messages={'required': 'Need Bing maps key'}
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'method', 'points',
                  'heights', 'samples', 'o', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        """This method occurs after dumping the data into the class.

        Args:
            data (dict): dictionary of all the query values

        Returns:
            data (dict): ordered dict of all the values
        """
        query = []
        keys_to_be_removed = []
        for key, value in data.items():
            if key not in ['version', 'restApi', 'resourcePath']:
                if not key == 'method':
                    if key == 'points':
                        value = ','.join(str(val) for val in value)
                        keys_to_be_removed.append(key)
                    query.append('{0}={1}'.format(key, value))
                    keys_to_be_removed.append(key)
                keys_to_be_removed.append(key)
        querystring = '&'.join(query)
        data['query'] = '{0}?{1}'.format(data['method'], querystring)
        for k in list(set(keys_to_be_removed)):
            del data[k]
        return data


class Offset(Elevations, Schema):
    """Inherited from :class:`Elevations`

    Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Data Fields for the schema (taken from
    https://msdn.microsoft.com/en-us/library/jj158961.aspx:

    :ivar method[Required]: A method for calculating elevations
        (ex. List/Polyline/SeaLevel/Bounds) - REQUIRED field
          - 'SeaLevel' [default]: Use this for returning elevations for a given
            pair of coordinates.
    :ivar points[Required]:  A set of coordinates on the Earth to use in
        elevation calculations. The exact use of these points depends on the
        type of elevation request. A set of latitude and longitude values in
        WGS84 decimal degrees. If you are requesting elevations or elevation
        offsets for a set of points, the maximum number of points is 1024.
        Points should be given as ``lat1,long1,lat2,long2,latn,longn`` -
        REQUIRED field
    :ivar o[Optional]: A string specifying the output as JSON or xml.
    :ivar key[Required: Bing maps key - REQUIRED field

    This schema helps in serializing the data.

    Post-Dump:
        After dumping the data, build_query_string builds up the
        queryParameters string. The final value after dumping the data would
        be a string.

    Example:

        ::

            >>> data = {'method': 'SeaLevel',
            ...         'points': [15.5467, 34.5676],
            ...         'key': 'abs'}
            >>> schema = Offset()
            >>> schema.dump(data).data
            OrderedDict([('version', 'v1'), ('restApi', 'Elevation'), ('query\
', 'SeaLevel?points=15.5467,34.5676&key=abs')])
    """
    method = fields.Str(
        required=True,
        validate=validate.Equal(
            'SeaLevel',
            error='The method should be SeaLevel'
        ),
        error_messages={'required': 'method for calculating elevations should'
                                    'be specified'}
    )
    points = fields.List(
        fields.Float,
        validate=validate.Length(
            min=2,
            error='Both latitude and longitude should be entered'
        ),
        required=True,
        error_messages={'required': 'Latitudes, Longitudes not specified'}
    )
    o = fields.Str()
    key = fields.Str(
        required=True,
        error_messages={'required': 'Need Bing maps key'}
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'method', 'points',
                  'o', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        """This method occurs after dumping the data into the class.

        Args:
            data (dict): dictionary of all the query values

        Returns:
            data (dict): ordered dict of all the values
        """
        query = []
        keys_to_be_removed = []
        for key, value in data.items():
            if key not in ['version', 'restApi', 'resourcePath']:
                if not key == 'method':
                    if key == 'points':
                        value = ','.join(str(val) for val in value)
                        keys_to_be_removed.append(key)
                    query.append('{0}={1}'.format(key, value))
                    keys_to_be_removed.append(key)
                keys_to_be_removed.append(key)
        querystring = '&'.join(query)
        data['query'] = '{0}?{1}'.format(data['method'], querystring)
        for k in list(set(keys_to_be_removed)):
            del data[k]
        return data


class BoundingBox(Elevations, Schema):
    """Inherited from :class:`Elevations`

    Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Data Fields for the schema (taken from
    https://msdn.microsoft.com/en-us/library/jj158961.aspx:

    :ivar method[Required]: A method for calculating elevations
        (ex. List/Polyline/SeaLevel/Bounds) - REQUIRED field
          - 'Bounds' [default]: Use this for returning elevations for a given
            pair of coordinates.
    :ivar bounds[Required]: Specifies the rectangular area over which to
        provide elevation values. A bounding box defined as a set of WGS84
        latitudes and longitudes in the following order:
          - south latitude, west longitude, north latitude, east longitude
          - REQUIRED field
    :ivar rows,cols[Required]: Specifies the number of rows and columns to use
        to divide the bounding box area into a grid. The rows and columns that
        define the bounding box each count as two (2) of the rows and columns.
        Elevation values are returned for all vertices of the grid. Integers
        with a value of two (2) or greater. The number of rows and columns
        can define a maximum of 1024 locations (rows * cols <= 1024).
    :ivar heights[Optional]: A string that specifies which sea level model to
        use to calculate elevation. One of the following values:
          - sealevel [default]: Use the geoid Earth model (EGM2008 2.5’).
          - ellipsoid: Use the ellipsoid Earth model (WGS84).
    :ivar o[Optional]: A string specifying the output as JSON or xml.
    :ivar key[Required]: Bing maps key

    This schema helps in serializing the data.

    Post-Dump:
        After dumping the data, build_query_string builds up the
        queryParameters string. The final value after dumping the data would
        be a string.

    Example:

        ::

            >>> data = {'method': 'Bounds',
            ...         'bounds': [15.5463, 34.6577, 16.4365, 35.3245],
            ...         'rows': 4,
            ...         'cols': 5,
            ...         'key': 'abs'}
            >>> schema = BoundingBox()
            >>> schema.dump(data).data
            OrderedDict([('version', 'v1'), ('restApi', 'Elevation'), ('query\
', 'Bounds?bounds=15.5463,34.6577,16.4365,35.3245&rows=4&cols=5&heights=\
sealevel&key=abs')])
    """
    method = fields.Str(
        required=True,
        validate=validate.Equal(
            'Bounds',
            error='The method should be Bounds'
        ),
        error_messages={'required': 'method for calculating elevations should'
                                    'be specified'}
    )
    bounds = fields.List(
        fields.Float,
        validate=validate.Length(
            min=4,
            max=4,
            error='All four should be entered: south latitude, west longitude,'
                  'north latitude and east longitude'
        ),
        required=True,
        error_messages={'required': 'Bounds not specified'}
    )
    rows = fields.Int(
        required=True,
        error_messages={'required': 'Number of rows should be specified'}
    )
    cols = fields.Int(
        required=True,
        error_messages={'required': 'Number of columns should be specified'}
    )
    heights = fields.Str(
        default='sealevel'
    )
    o = fields.Str()
    key = fields.Str(
        required=True,
        error_messages={'required': 'Need bing maps key'}
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'method', 'bounds',
                  'rows', 'cols', 'heights', 'o', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        """This method occurs after dumping the data into the class.

        Args:
            data (dict): dictionary of all the query values

        Returns:
            data (dict): ordered dict of all the values
        """
        query = []
        keys_to_be_removed = []
        for key, value in data.items():
            if key not in ['version', 'restApi', 'resourcePath']:
                if not key == 'method':
                    if key == 'bounds':
                        value = ','.join(str(val) for val in value)
                        keys_to_be_removed.append(key)
                    query.append('{0}={1}'.format(key, value))
                    keys_to_be_removed.append(key)
                keys_to_be_removed.append(key)
        querystring = '&'.join(query)
        data['query'] = '{0}?{1}'.format(data['method'], querystring)
        for k in list(set(keys_to_be_removed)):
            del data[k]
        return data
