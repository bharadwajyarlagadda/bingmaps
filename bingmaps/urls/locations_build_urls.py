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
        """This property helps in returning the http protocol to be used as
        part of the URL.

        :ivar http_protocol: The http protocol passed in (http/https)

        :getter: Returns a string relevant to the http
            protocol
              - http: ``http:/``
              - https: ``https:/``
        :type: string
        """
        if self._http_protocol == 'http':
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
              - ``v1`` for Locations services
        :type: string
        """
        if 'version' in self._schema_dict:
            return self._schema_dict['version']
        else:
            return None

    @property
    def restApi(self):
        """This property gives a part of the URL that identifies the REST API

        :getter: Returns a part of the URL that identifies the REST
            API
              - ``Locations`` for Locations services
        :type: string
        """
        if 'restApi' in self._schema_dict:
            return self._schema_dict['restApi']
        else:
            return None

    @property
    def resourcePath(self):
        """This property gives a part of the URL that specifies a resource
        such as an address or landmark.

        :getter: Returns a string that identifies the resource path such as
            address or landmark
              - ``None`` for Locations services
        :type: string
        """
        if 'resourcePath' in self._schema_dict:
            return self._schema_dict['resourcePath']
        else:
            return None


class Location(Schema):
    """Main class for Locations API schema

    Data Fields:

    :ivar version: A string containing v and an integer that specifies
        the version of the Bing Maps REST Services.
          - default: v1
    :ivar restApi: A part of the URL path that identifies the REST
        API.
          - default: 'Locations' (for Locations API services)
    :ivar resourcePath: A part of the URL path that specifies a
        resource, such as an address or landmark.

    This schema helps in creating the main parameters of all types of locations
    API based services (location by address, location by point, location by
    query. The above mentioned data fields make up the main parameters of the
    url.

    Example:
        The below example can show you a typical example for how the main URL
        parameters can be passed in as a dictionary
        ::

            >>> data = {'version': 'v1',
            ...         'restApi': 'Locations',
            ...         'resourcePath': ''}

        When you dump an empty dictionary, the class helps you in filling the
        dictionary with default values. You can see the same behaviour in the
        below example:

        ::

            >>> data = {}
            >>> schema = Location()
            >>> schema.dump(data).data
            OrderedDict([('version', 'v1'), ('restApi', 'Locations')])

    .. note:: Location class is common for all the location based services
        with the same default data.
    """
    version = fields.Str(
        default='v1'
    )
    restApi = fields.Str(
        default='Locations'
    )
    resourcePath = fields.Str()

    class Meta:
        """Meta class helps in ordering all the fields in the specified order
        """
        fields = ('version', 'restApi', 'resourcePath')
        ordered = True


class LocationByAddressSchema(Location, Schema):
    """Inherits from :class:`Location`

    Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Data Fields for the schema (taken from
    https://msdn.microsoft.com/en-us/library/ff701714.aspx):

    :ivar adminDistrict[Optional]: A string that contains a subdivision, such
        as the abbreviation of a US state
    :ivar locality[Optional]: A string that contains the locality, such as a
        US city
    :ivar postalCode[Optional]: An integer value that contains the postal
        code, such as a US ZIP Code
    :ivar addressLine[Optional]: A string specifying the street line of an
        address
    :ivar countryRegion[Optional]: A string specifying the ISO country code
    :ivar c[Optional]: A string specifying the culture parameter
    :ivar o[Optional]: A string for specifying the format of output(response)
        Ex. - xml/json
          - If empty, default output would be a JSON data string
          - If given xml, the output would be an xml data string
    :ivar includeNeighborhood[Optional]: One of the following
        values
          - 1: Include neighborhood information when available
          - 0 [default]: Do not include neighborhood information
    :ivar include[Optional]: The only value for this parameter is ciso2. When
        you specify include=ciso2, the two-letter ISO country code is included
        for addresses in the response
          - default='ciso2'
    :ivar maxResults[Optional]: An integer between 1 and 20 (number of
        results)
          - default=20
    :ivar key[Required]: Bing maps api key
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
            >>> query = LocationByAddressSchema()
            >>> query.dump(data).data
            OrderedDict([('version', 'v1'), ('restApi', 'Locations'), ('query\
', 'adminDistrict=WA&locality=Seattle&c=te&o=xml&\
includeNeighborhood=1&include=ciso2&maxResults=20&key=abs')])

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
        fields = ('version', 'restApi', 'resourcePath',
                  'adminDistrict', 'locality', 'postalCode',
                  'addressLine', 'countryRegion', 'c', 'o',
                  'includeNeighborhood', 'include', 'maxResults', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        """This method occurs after dumping the data into the class.

        Args:
            data (dict): dictionary of all the query values

        Returns:
            data (dict): ordered dict of all the values
        """
        query_params = []
        keys_to_be_removed = []
        for key, value in data.items():
            if key not in ['version', 'restApi', 'resourcePath']:
                if key == 'addressLine':
                    query_params.append('{0}={1}'.format(key,
                                                         quote(value)))
                    keys_to_be_removed.append(key)
                else:
                    query_params.append('{0}={1}'.format(key,
                                                         value))
                    keys_to_be_removed.append(key)
        data['query'] = "&".join(query_params)
        for k in keys_to_be_removed:
            del data[k]
        return data


class LocationByAddressUrl(LocationUrl):
    """This class helps in building a url for location by address service.

    :ivar data: Data required for building up the URL
    :ivar httpprotocol: http protocol for the url
    :ivar schema: location by address schema to which the data will be dumped

    All the URL values are retrieved from the schema.

    Example:

        ::

            >>> data = { 'adminDistrict': 'WA',
            ...          'locality': 'Seattle',
            ...          'c': 'te',
            ...          'o': 'xml',
            ...          'includeNeighborhood': 1,
            ...          'key': 'abs'}
            >>> loc_by_address = LocationByAddressUrl(data, 'http')
            >>> loc_by_address.main_url
            'dev.virtualearth.net'
            >>> loc_by_address.protocol
            'http:/'
            >>> loc_by_address.resourcePath

            >>> loc_by_address.restApi
            'Locations'
            >>> loc_by_address.rest
            'REST'
            >>> loc_by_address.version
            'v1'
            >>> loc_by_address.query
            '?adminDistrict=WA&locality=Seattle&c=te&o=xml&\
includeNeighborhood=1&include=ciso2&maxResults=20&key=abs'
    """
    def __init__(self, data, httpprotocol):
        schema = LocationByAddressSchema()
        super().__init__(data, httpprotocol, schema)

    @property
    def query(self):
        """This property helps in retrieving the query part of the URL

        :getter: Returns a part of the URL which consist of all the query
            parameters. The query is formatted with a ``?`` in front of it.
        :type: string
        """
        return '?{0}'.format(self._schema_dict['query'])


class LocationByPointSchema(Location, Schema):
    """Inherits from :class:`Location`

    Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Data Fields for the schema (taken from
    https://msdn.microsoft.com/en-us/library/ff701710.aspx):

    :ivar point[Required]: A point on the Earth specified by a latitude and
        longitude.
    :ivar includeEntityTypes[Optional]: A comma separated list of entity types
        selected from the following options:
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
    :ivar includeNeighborhood[Optional]: One of the following
        values:
          - 1: Include neighborhood information when available.
          - 0 [default]: Do not include neighborhood information.
    :ivar include[Optional]: The only value for this parameter is ciso2. When
        you specify include=ciso2, the two-letter ISO country code is included
        for addresses in the response.
    :ivar c[Optional]: A string specifying the culture parameter
    :ivar o[Optional]: A string for specifying the format of output(response)
        Ex. - xml/json
          - If empty, default output would be a JSON data string
          - If given xml, the output would be an xml data string
    :ivar maxResults[Optional]: An integer between 1 and 20 (number of
        results)
          - default=20
    :ivar key[Required]: Bing maps api
        key
          - Required

    Post-Dump:
        After dumping the data, build_query_string builds up the
        queryParameters string. The final value after dumping the data would
        be a string. The string would be similar to the one mentioned in the
        below example.

    Example:

        ::

            >>> data = { 'point': '47.64054,-122.12934',
            ...          'includeEntityTypes': 'Address',
            ...          'c': 'te',
            ...          'o': 'xml',
            ...          'includeNeighborhood': 1,
            ...          'key': 'abs'
            ...         }
            >>> query = LocationByPointSchema()
            >>> query.dump(data).data
            OrderedDict([('version', 'v1'), ('restApi', 'Locations'), ('query\
', '47.64054,-122.12934?includeEntityTypes=Address&\
includeNeighborhood=1&include=ciso2&c=te&o=xml&maxResults=20&key=abs')])


        In the output, you can see 'include', 'maxResults' in the string
        although we haven't specified any values because they are default
        values specified in the schema.
    """
    point = fields.Str(
        required=True,
        error_messages={'required': 'coordinates should be provided'}
    )
    includeEntityTypes = fields.Str()
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

    class Meta:
        fields = ('version', 'restApi', 'resourcePath',
                  'point', 'includeEntityTypes', 'includeNeighborhood',
                  'include', 'c', 'o', 'maxResults', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        """This method occurs after dumping the data into the class.

        Args:
            data (dict): dictionary of all the query values

        Returns:
            data (dict): ordered dict of all the values
        """
        queryValues = []
        keys_to_be_removed = []
        for key, value in data.items():
            if key not in ['version', 'restApi', 'resourcePath']:
                if not key == 'point':
                    queryValues.append('{0}={1}'.format(key, value))
                    keys_to_be_removed.append(key)
                keys_to_be_removed.append(key)
        queryString = '&'.join(queryValues)
        data['query'] = '{0}?{1}'.format(data['point'], queryString)
        for k in list(set(keys_to_be_removed)):
            del data[k]
        return data


class LocationByPointUrl(LocationUrl):
    """This class helps in building a url for location by point service.

    :ivar data: Data required for building up the URL
    :ivar httpprotocol: http protocol for the url
    :ivar schema: location by point schema to which the data will be dumped

    All the URL values are retrieved from the schema.

    Example:

        ::

            >>> data = { 'point': '47.64054,-122.12934',
            ...          'includeEntityTypes': 'Address',
            ...          'c': 'te',
            ...          'o': 'xml',
            ...          'includeNeighborhood': 1,
            ...          'key': 'abs'}
            >>> loc_by_point = LocationByPointUrl(data, 'http')
            >>> loc_by_point.main_url
            'dev.virtualearth.net'
            >>> loc_by_point.protocol
            'http:/'
            >>> loc_by_point.resourcePath

            >>> loc_by_point.restApi
            'Locations'
            >>> loc_by_point.rest
            'REST'
            >>> loc_by_point.version
            'v1'
            >>> loc_by_point.query
            '47.64054,-122.12934?includeEntityTypes=Address&\
includeNeighborhood=1&include=ciso2&c=te&o=xml&maxResults=20&key=abs'
    """
    def __init__(self, data, httpprotocol):
        schema = LocationByPointSchema()
        super().__init__(data, httpprotocol, schema)

    @property
    def query(self):
        """This property helps in retrieving the query part of the URL

        :getter: Returns a part of the URL which consist of all the query
            parameters
        :type: string
        """
        return self._schema_dict['query']


class LocationByQuerySchema(Location, Schema):
    """Inherits from :class:`Location`

    Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Data Fields for the schema (taken from
    https://msdn.microsoft.com/en-us/library/ff701711.aspx):

    :ivar q[Required]: A string (query) that contains information about a
        location, such as an address or landmark name.
    :ivar includeNeighborhood[Optional]: One of the following
        values:
          - 1: Include neighborhood information when available.
          - 0 [default]: Do not include neighborhood information.
    :ivar include[Optional]: One or more of the following
        options:
          - queryParse: Specifies that the response shows how the query string
            was parsed into address values, such as addressLine, locality,
            adminDistrict, and postalCode.
          - ciso2: Specifies to include the two-letter ISO country code.
        If you specify more than one include value, separate the values with a
        comma.
    :ivar c[Optional]: A string specifying the culture parameter
    :ivar o[Optional]: A string for specifying the format of output(response)
        Ex. - xml/json
          - If empty, default output would be a JSON data string
          - If given xml, the output would be an xml data string
    :ivar maxResults[Optional]: An integer between 1 and 20 (number of
        results)
          - default=20
    :ivar key[Required]: Bing maps api
        key
          - Required

    Post-Dump:
        After dumping the data, build_query_string builds up the
        queryParameters string. The final value after dumping the data would
        be a string. The string would be similar to the one mentioned in the
        below example.

    Example:

        ::

            >>> data = {'q': '1014 Oatney Ridge Ln., Morrisville,NC-27560',
            ...         'key': 'abs'}
            >>> query = LocationByQuerySchema()
            >>> query.dump(data).data
            OrderedDict([('version', 'v1'), ('restApi', 'Locations'), ('query\
', 'q=1014%20Oatney%20Ridge%20Ln.%2C%20Morrisville\
%2CNC-27560&includeNeighborhood=0&include=ciso2&maxResults=20&key=abs')])

        In the output, you can see 'include', 'maxResults' in the string
        although we haven't specified any values because they are default
        values specified in the schema.
    """
    q = fields.Str(
        required=True,
        error_messages={'required': 'require a query string'}
    )
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

    class Meta:
        fields = ('version', 'restApi', 'resourcePath',
                  'q', 'includeNeighborhood', 'include', 'c', 'o',
                  'maxResults', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        """This method occurs after dumping the data into the class.

        Args:
            data (dict): dictionary of all the query values

        Returns:
            data (dict): ordered dict of all the values

        The query string consists of all the values concatenated
        with '&'. As part of the location by query services, the url will
        be encoded. If the 'query' consists of spaces, commas, or other
        special characters all those will be encoded.

        For example:
          - space(' ') - %20
          - comma(,) - %2C, etc.
        """
        query_params = []
        keys_to_be_removed = []
        for key, value in data.items():
            if key not in ['version', 'restApi', 'resourcePath']:
                if key == 'q':
                    query_params.append('{0}={1}'.format(key,
                                                         quote(value)))
                    keys_to_be_removed.append(key)
                else:
                    query_params.append('{0}={1}'.format(key,
                                                         value))
                    keys_to_be_removed.append(key)
        for k in list(set(keys_to_be_removed)):
            del data[k]
        data['query'] = "&".join(query_params)
        return data


class LocationByQueryUrl(LocationUrl):
    """This class helps in building a url for location by query service.

    :ivar data: Data required for building up the URL
    :ivar httpprotocol: http protocol for the url
    :ivar schema: location by query schema to which the data will be dumped

    All the URL values are retrieved from the schema.

    Example:

        ::

            >>> data = {'q': '1014 Oatney Ridge Ln.,Morrisville,NC-27560',
            ...         'key': 'abs'}
            >>> loc_by_query = LocationByQueryUrl(data, 'http')
            >>> loc_by_query.main_url
            'dev.virtualearth.net'
            >>> loc_by_query.protocol
            'http:/'
            >>> loc_by_query.resourcePath

            >>> loc_by_query.restApi
            'Locations'
            >>> loc_by_query.rest
            'REST'
            >>> loc_by_query.version
            'v1'
            >>> loc_by_query.query
            '?q=1014%20Oatney%20Ridge%20Ln.%2CMorrisville\
%2CNC-27560&includeNeighborhood=0&include=ciso2&maxResults=20&key=abs'
    """
    def __init__(self, data, httpprotocol):
        schema = LocationByQuerySchema()
        super().__init__(data, httpprotocol, schema)

    @property
    def query(self):
        """This property helps in retrieving the query part of the URL

        :getter: Returns a part of the URL which consist of all the query
            parameters. The query is formatted with a ``?`` in front of it.
        :type: string
        """
        return '?{0}'.format(self._schema_dict['query'])
