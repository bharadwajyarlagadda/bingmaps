from marshmallow import Schema, fields, post_dump, validate, pre_dump


class TrafficIncidentsUrl(object):
    """This class helps in building a url for elevations API service.

    :ivar data: Data required for building up the URL
    :ivar protocol: http protocol for the url
    :ivar schema: Elevations schema to which the data will be dumped

    All the URL values are retrieved from the schema.

    Example:

        ::

            >>> data = {'mapArea': [37, -105, 45, -94],
            ...         'includeLocationCodes': 'true',
            ...         'type': [5],
            ...         'o': 'xml',
            ...         'key': 'abs'}
            >>> url = TrafficIncidentsUrl(data, TrafficIncidentsSchema(),
            ...                           'http')
            >>> url.main_url
            'dev.virtualearth.net'
            >>> url.protocol
            'http:/'
            >>> url.resourcePath
            'Incidents'
            >>> url.restApi
            'Traffic'
            >>> url.rest
            'REST'
            >>> url.version
            'v1'
            >>> url.query
            '37.0,-105.0,45.0,-94.0/true?type=5&o=xml&key=abs'
    """
    def __init__(self, data, schema, protocol='http'):
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


class MainParams(Schema):
    version = fields.Constant(
        'v1',
        required=True
    )
    restApi = fields.Constant(
        'Traffic',
        required=True
    )
    resourcePath = fields.Constant(
        'Incidents',
        required=True
    )


class TrafficIncidentsSchema(MainParams, Schema):
    """Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Data Fields for the schema (taken from
    https://msdn.microsoft.com/en-us/library/hh441726.aspx):

    :ivar mapArea[Required]: A rectangular area specified as a bounding box.
        The size of the area can be a maximum of 500 km x 500 km. A bounding
        box defines an area by specifying SouthLatitude, WestLongitude,
        NorthLatitude, and EastLongitude values.
    :ivar includeLocationCodes[Optional]:  One of the following
        values:
          - 'true'
          - 'false' [default]
        If you want to use the default value, you can omit this parameter from
        the URL request.
    :ivar severity[Optional]: One or more of the following integer
        values:
          - 1: LowImpact
          - 2: Minor
          - 3: Moderate
          - 4: Serious
        The default is to return traffic incidents for all severity levels.
    :ivar type[Optional]: One or more of the following integer
        values:
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
    :ivar o[Optional]: A string specifying the output as JSON or xml.
    :ivar key[Required]: Bing maps key - REQUIRED field

    This schema helps in serializing the data.

    Post-Dump:
        After dumping the data, build_query_string builds up the
        queryParameters string. The final value after dumping the data would
        be a string.

    Example:

        ::

            >>> data = {'mapArea': [37, -105, 45, -94],
            ...         'includeLocationCodes': 'true',
            ...         'type': [5],
            ...         'o': 'xml',
            ...         'key': 'abs'}
            >>> query = TrafficIncidentsSchema()
            >>> query.dump(data).data
            OrderedDict([('version', 'v1'), ('restApi', 'Traffic'), \
('resourcePath', 'Incidents'), ('query', \
'37.0,-105.0,45.0,-94.0/true?type=5&o=xml&key=abs')])
    """
    mapArea = fields.List(
        fields.Float,
        required=True,
        error_messages={'required': 'All the four coordinates required'},
        validate=validate.Length(
            min=4,
            max=4,
            error='All the four coordinates should be entered: south latitude,'
                  'west longitude, north latitude and east longitude in the '
                  'same order'
        )
    )
    includeLocationCodes = fields.Str(
        default='false'
    )
    severity = fields.List(
        fields.Int
    )
    type = fields.List(
        fields.Int
    )
    o = fields.Str()
    key = fields.Str(
        required=True,
        error_messages={'required': 'Bing Maps API key required'}
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'mapArea',
                  'includeLocationCodes', 'severity', 'type', 'o', 'key')
        ordered = True

    @post_dump
    def build_url(self, data):
        """This method occurs after dumping the data into the class.

        Args:
            data (dict): dictionary of all the query values

        Returns:
            data (dict): ordered dict of all the values
        """
        query_part_one = []
        query_part_two = []
        keys_to_be_removed = []
        for key, value in data.items():
            if key not in ['version', 'restApi', 'resourcePath']:
                if key == 'mapArea':
                    query_part_one.append(','.join(str(val) for val in value))
                    keys_to_be_removed.append(key)
                elif key == 'includeLocationCodes':
                    query_part_one.append(value)
                    keys_to_be_removed.append(key)
                else:
                    if isinstance(value, list):
                        value = ','.join(str(val) for val in value)
                    query_part_two.append('{0}={1}'.format(key, value))
                    keys_to_be_removed.append(key)
        for k in keys_to_be_removed:
            del data[k]
        data['query'] = '{0}?{1}'.format('/'.join(query_part_one),
                                         '&'.join(query_part_two))
        return data
