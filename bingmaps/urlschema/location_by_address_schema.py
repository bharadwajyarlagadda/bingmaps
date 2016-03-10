from marshmallow import Schema, fields, post_dump
from .location_schema import Location
from .location_api_url import LocationUrl


class LocationByAddressQueryString(Schema):
    """Schema for query parameters in which all the fields will be in a ordered
    way. All the fields will be dumped in the same order as mentioned in the
    schema.

    Post-Dumping the data: A query string will be constructed with all the
    fields.

    Data Fields for query schema:
        adminDistrict (str): A string that contains a subdivision, such
            as the abbreviation of a US state
        locality (str): A string that contains the locality, such as a US city
        postalCode (int): A string that contains the postal code, such as a
            US ZIP Code
        addressLine (str): A string specifying the street line of an address
        countryRegion (str): A string specifying the ISO country code
        o (str): Format of the output file. Ex. xml or json
        includeNeighborhood (str): One of the following values:
            1: Include neighborhood information when available.
            0 [default]: Do not include neighborhood information.
        include (str): The only value for this parameter is ciso2. When you
            specify include=ciso2, the two-letter ISO country code is included
            for addresses in the response.
        maxResults (int): A string that contains an integer between 1 and 20.
            The default value is 5
        key (str): Bing maps api key

    This schema helps in serializing the data.

    Post-Dump Data:
        After dumping the data, build_query_string builds up the query for
        queryParameters. The final value after dumping the data would be a
        string.
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
