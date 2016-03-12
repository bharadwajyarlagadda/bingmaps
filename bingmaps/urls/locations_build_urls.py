from marshmallow import Schema, fields, post_dump
from urllib.parse import quote


class LocationUrl(object):
    def __init__(self, data, protocol, schema):
        self._data = data
        self._http_protocol = protocol
        self._schema_dict = self._schema_values(schema)

    def _schema_values(self, schema):
        is_valid_schema = schema.validate(self._data)
        if bool(is_valid_schema):
            raise KeyError(is_valid_schema)
        else:
            return schema.dump(self._data).data

    @property
    def protocol(self):
        if self._http_protocol == 'http':
            return 'http:/'
        else:
            return 'https:/'

    @property
    def main_url(self):
        return 'dev.virtualearth.net'

    @property
    def rest(self):
        return 'REST'

    @property
    def version(self):
        if 'version' in self._schema_dict:
            return self._schema_dict['version']
        else:
            return None

    @property
    def restApi(self):
        if 'restApi' in self._schema_dict:
            return self._schema_dict['restApi']
        else:
            return None

    @property
    def resourcePath(self):
        if 'resourcePath' in self._schema_dict:
            return self._schema_dict['resourcePath']
        else:
            return None


class Location(Schema):
    """Main class for Locations API schema

    Data Fields:

        * version (str):
        * restApi (str): The API which is being
          used
            - default: Locations for Locations API services
    """
    version = fields.Str(
        default='v1'
    )
    restApi = fields.Str(
        default='Locations'
    )
    resourcePath = fields.Str()


class LocationByAddressQueryString(Schema):
    """Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Data Fields for the schema:

        * adminDistrict (str): A string that contains a subdivision, such
          as the abbreviation of a US state
        * locality (str): A string that contains the locality, such as a US
          city
        * postalCode (int): A string that contains the postal code, such as a
          US ZIP Code
        * addressLine (str): A string specifying the street line of an address
        * countryRegion (str): A string specifying the ISO country code
        * c (str): A string specifying the culture parameter
        * o (str): Format of the output file
          (Example - xml/json)
            - If empty, default output would be a JSON data string
            - If given xml, the output would be an xml data string
        * includeNeighborhood (str): One of the following
          values
            - 1: Include neighborhood information when available
            - 0 [default]: Do not include neighborhood information
        * include (str): The only value for this parameter is ciso2. When you
          specify include=ciso2, the two-letter ISO country code is included
          for addresses in the response
            - default='ciso2'
        * maxResults (int): A string that contains an integer between 1 and 20.
          The default value is 5
            - default=20
        * key (str): Bing maps api
          key
            - Required

    This schema helps in serializing the data.

    Post-Dump:
        After dumping the data, build_query_string builds up the
        queryParameters string. The final value after dumping the data would
        be a string.

    Example:

        ::

            >>> data = { 'adminDistrict': 'WA',
            ...          'locality': 'Seattle',
            ...          'c': 'te',
            ...          'o': 'xml',
            ...          'includeNeighborhood': 1,
            ...          'key': 'abs'
            ...         }
            >>> query = LocationByAddressQueryString()
            >>> query.dump(data).data
            'adminDistrict=WA&locality=Seattle&c=te&o=xml&includeNeighborhood=1&include=ciso2&maxResults=20&key=abs'

        In the output, you can see 'include', 'maxResults' in the string
        although we haven't specified any values because they are default
        values specified in the schema.
    """
    adminDistrict = fields.Str()
    locality = fields.Str()
    postalCode = fields.Int()
    addressLine = fields.Str()
    countryRegion = fields.Str()
    c = fields.Str()
    o = fields.Str()
    includeNeighborhood = fields.Int(
        default=0
    )
    include = fields.Str(
        default='ciso2'
    )
    maxResults = fields.Int(
        default=20
    )
    key = fields.Str(
        required=True,
        error_messages={'required': 'Please provide a key'}
    )

    class Meta:
        """Meta class helps in ordering all the fields in the specified order
        """
        fields = ('adminDistrict', 'locality', 'postalCode',
                  'addressLine', 'countryRegion', 'c', 'o',
                  'includeNeighborhood', 'include', 'maxResults', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        """This method occurs after dumping the data into the class.

        Args:
            data (dict): dictionary of all the query values

        Returns:
            str: query string consisting of all the values concatenated
            with '&'
        """
        query_params = []
        for key, value in data.items():
            query_params.append('{0}={1}'.format(key,
                                                 value))
        return "&".join(query_params)


class LocationByAddressSchema(Location, Schema):
    """Inherits from Location schema.
    """
    queryParameters = fields.Nested(
        LocationByAddressQueryString
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'queryParameters')
        ordered = True


class LocationByAddressUrl(LocationUrl):
    """Inherits from LocationUrl class. This class helps in build a url for
    LocationByAddress API.

    The url format for location by address API would be (unstructured
    URL format):
        http://dev.virtualearth.net/REST/v1/Locations?countryRegion=
        countryRegion&adminDistrict=adminDistrict&locality=
        locality&postalCode=postalCode&addressLine=addressLine&userLocation=
        userLocation&userIp=userIp&usermapView=usermapView&
        includeNeighborhood=includeNeighborhood&maxResults=
        maxResults&key=BingMapsKey

    All the URL values are retrieved from the schema.
    """
    def __init__(self, data, protocol):
        schema = LocationByAddressSchema()
        super().__init__(data, protocol, schema)

    @property
    def query(self):
        return '?{0}'.format(self._schema_dict['queryParameters'])


class LocationByPointQueryString(Schema):
    """Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.


    """
    point = fields.Str()
    includeEntityTypes = fields.Str()
    includeNeighborhood = fields.Int(
        default=0
    )
    include = fields.Str(
        default='ciso2'
    )
    c = fields.Str()
    o = fields.Str()
    key = fields.Str(
        required=True,
        error_messages={'required': 'Please provide a key'}
    )

    class Meta:
        fields = ('point', 'includeEntityTypes', 'includeNeighborhood',
                  'include', 'c', 'o', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        queryValues = []
        for key, value in data.items():
            if not key == 'point':
                queryValues.append('{0}={1}'.format(key, value))
        queryString = '&'.join(queryValues)
        return '{0}?{1}'.format(data['point'], queryString)


class LocationByPointSchema(Location, Schema):
    queryParameters = fields.Nested(
        LocationByPointQueryString
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'queryParameters')
        ordered = True


class LocationByPointUrl(LocationUrl):
    def __init__(self, data, protocol):
        schema = LocationByPointSchema()
        super().__init__(data, protocol, schema)

    @property
    def query(self):
        return self._schema_dict['queryParameters']


class LocationByQueryString(Schema):
    query = fields.Str()
    includeNeighborhood = fields.Int(
        default=0
    )
    include = fields.Str(
        default='ciso2'
    )
    c = fields.Str()
    o = fields.Str()
    maxResults = fields.Int(
        default=20
    )
    key = fields.Str(
        required=True,
        error_messages={'required': 'Please provide a key'}
    )

    class Meta():
        fields = ('query', 'includeNeighborhood', 'include', 'c', 'o',
                  'maxResults', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        query_params = []
        for key, value in data.items():
            if key == 'query':
                query_params.append('{0}={1}'.format(key,
                                                     quote(value)))
            else:
                query_params.append('{0}={1}'.format(key,
                                                     value))

        return "&".join(query_params)


class LocationByQuerySchema(Location, Schema):
    queryParameters = fields.Nested(
        LocationByQueryString
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'queryParameters')
        ordered = True


class LocationByQueryUrl(LocationUrl):
    def __init__(self, data, protocol):
        schema = LocationByQuerySchema()
        super().__init__(data, protocol, schema)

    @property
    def query(self):
        return '?{0}'.format(self._schema_dict['queryParameters'])
