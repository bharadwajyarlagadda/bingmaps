from .location_schema import Location
from marshmallow import Schema, fields, post_dump
from .location_api_url import LocationUrl


class LocationByPointQueryString(Schema):
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
                  'include', 'o', 'key')
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
