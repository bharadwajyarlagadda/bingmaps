from marshmallow import fields, Schema, post_dump, validate


class ElevationsUrl(object):
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
            parameters. The query is formatted with a ``?`` in front of it.
        :type: string
        """
        return self.schema_dict['queryParameters']


class Elevations(Schema):
    version = fields.Str(
        default='v1'
    )
    restApi = fields.Str(
        default='Elevation'
    )
    resourcePath = fields.Str()

    class Meta:
        """Meta class helps in ordering all the fields in the specified order
        """
        fields = ('version', 'restApi', 'resourcePath')
        ordered = True


class Coordinates(Schema):
    method = fields.Str(
        required=True,
        validate=validate.Equal(
            'List',
            error='The method should be Bounds'
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
        fields = ('method', 'points', 'heights', 'o', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        query = []
        for key, value in data.items():
            if not key == 'method':
                if key == 'points':
                    value = ','.join(str(val) for val in value)
                query.append('{0}={1}'.format(key, value))
        querystring = '&'.join(query)
        return '{0}?{1}'.format(data['method'], querystring)


class CoordinatesSchema(Elevations, Schema):
    queryParameters = fields.Nested(
        Coordinates
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'queryParameters')
        ordered = True


class Polyline(Elevations, Schema):
    method = fields.Str(
        required=True,
        validate=validate.Equal(
            'Polyline',
            error='The method should be Bounds'
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
        fields = ('method', 'points', 'heights', 'samples', 'o', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        query = []
        for key, value in data.items():
            if not key == 'method':
                if key == 'points':
                    value = ','.join(str(val) for val in value)
                query.append('{0}={1}'.format(key, value))
        querystring = '&'.join(query)
        return '{0}?{1}'.format(data['method'], querystring)


class PolylineSchema(Elevations, Schema):
    queryParameters = fields.Nested(
        Polyline
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'queryParameters')
        ordered = True


class Offset(Schema):
    method = fields.Str(
        required=True,
        validate=validate.Equal(
            'SeaLevel',
            error='The method should be Bounds'
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
        fields = ('method', 'points', 'o', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        query = []
        for key, value in data.items():
            if not key == 'method':
                if key == 'points':
                    value = ','.join(str(val) for val in value)
                query.append('{0}={1}'.format(key, value))
        querystring = '&'.join(query)
        return '{0}?{1}'.format(data['method'], querystring)


class OffsetSchema(Elevations, Schema):
    queryParameters = fields.Nested(
        Offset
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'queryParameters')
        ordered = True


class BoundingBox(Schema):
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
        fields = ('method', 'bounds', 'rows', 'cols', 'heights', 'o', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        query = []
        for key, value in data.items():
            if not key == 'method':
                if key == 'bounds':
                    value = ','.join(str(val) for val in value)
                query.append('{0}={1}'.format(key, value))
        querystring = '&'.join(query)
        return '{0}?{1}'.format(data['method'], querystring)


class BoundingBoxSchema(Elevations, Schema):
    queryParameters = fields.Nested(
        BoundingBox
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'queryParameters')
        ordered = True
