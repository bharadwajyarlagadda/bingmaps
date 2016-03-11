from marshmallow import Schema, fields, post_dump
from .location_schema import Location
from urllib.parse import quote
from .location_api_url import LocationUrl


class LocationByQueryString(Schema):
    query = fields.Str()
    includeNeighborhood = fields.Int(
        default=0
    )
    include = fields.Str(
        default='ciso2'
    )
    o = fields.Str()
    maxResults = fields.Int(
        default=20
    )
    key = fields.Str(
        required=True,
        error_messages={'required': 'Please provide a key'}
    )

    class Meta():
        fields = ('query', 'includeNeighborhood', 'include', 'o',
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
