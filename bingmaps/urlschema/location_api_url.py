

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
