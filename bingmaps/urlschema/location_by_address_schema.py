from marshmallow import Schema, fields, post_dump


class LocationByAddressQueryString(Schema):
    """Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Post-Dumping the data: A query string will be constructed with all the
    fields.


    Data Fields for query schema::
        ``adminDistrict (str)``: A string that contains a subdivision, such
                                 as the abbreviation of a US state
        ``locality (str)``: A string that contains the locality, such as a US
                            city
        ``postalCode (int)``: A string that contains the postal code, such as a
                              US ZIP Code
        ``addressLine (str)``: A string specifying the street line of an
                               address
        ``countryRegion (str)``: A string specifying the ISO country code
        ``o (str)``: Format of the output file. Ex. xml or json
        ``includeNeighborhood (str)``: One of the following values:
                                       1: Include neighborhood information
                                          when available.
                                       0 [default]: Do not include neighborhood
                                                    information.
        ``include (str)``: The only value for this parameter is ciso2. When you
                           specify include=ciso2, the two-letter ISO country
                           code is included for addresses in the response.
        ``maxResults (int)``: A string that contains an integer between 1 and
                              20. The default value is 5
        ``key (str)``: Bing maps api key
    """
    adminDistrict = fields.Str()
    locality = fields.Str()
    postalCode = fields.Int()
    addressLine = fields.Str()
    countryRegion = fields.Str()
    o = fields.Str()
    includeNeighborhood = fields.Int(
        default=1
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
                  'addressLine', 'countryRegion', 'o', 'includeNeighborhood',
                  'include', 'maxResults', 'key')
        ordered = True

    @post_dump
    def build_query_string(self, data):
        """This method occurs after dumping the data into the class.

        ARGS::
            ``data (dict)``: dictionary of all the query values

        Returns::
            ``str``: query string consisting of all the values concatenated
                     with `&`
        """
        query_params = []
        for key, value in data.items():
            query_params.append('{0}={1}'.format(key,
                                                 value))
        return "&".join(query_params)


class Location(Schema):
    version = fields.Str(
        default='v1'
    )
    restApi = fields.Str(
        default='Locations'
    )
    resourcePath = fields.Str()


class LocationByAddressSchema(Location, Schema):
    queryParameters = fields.Nested(
        LocationByAddressQueryString
    )

    class Meta:
        fields = ('version', 'restApi', 'resourcePath', 'queryParameters')
        ordered = True


class LocationByAddressUrl(object):
    def __init__(self, data, protocol):
        self._data = data
        self._http_protocol = protocol
        self._schema_dict = self._schema_values()

    def _schema_values(self):
        schema = LocationByAddressSchema()
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
            return ''

    @property
    def restApi(self):
        if 'restApi' in self._schema_dict:
            return self._schema_dict['restApi']
        else:
            return ''

    @property
    def resourcePath(self):
        if 'resourcePath' in self._schema_dict:
            return self._schema_dict['resourcePath']
        else:
            return ''

    @property
    def query(self):
        return '?{0}'.format(self._schema_dict['queryParameters'])
