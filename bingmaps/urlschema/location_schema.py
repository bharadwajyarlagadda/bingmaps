from marshmallow import Schema, fields


class Location(Schema):
    version = fields.Str(
        default='v1'
    )
    restApi = fields.Str(
        default='Locations'
    )
    resourcePath = fields.Str()
