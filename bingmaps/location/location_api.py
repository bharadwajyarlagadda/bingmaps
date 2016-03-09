import json


class LocationApi(object):
    """Parent class for LocationByAddress and LocationByPoint api classes"""
    def __init__(self, schema, http_protocol='http'):
        self.http_protocol = http_protocol
        self.file_name = 'locationByAddress'
        self.locationApiData = None
        self.schema = schema

    def build_url(self):
        """Method for building a url based on the schema given

        Returns:
            url (str): http/https url for locations API
        """
        url = '{protocol}/{url}/{rest}/{version}/{restapi}/{rscpath}/' \
              '{query}'.format(protocol=self.schema.protocol,
                               url=self.schema.main_url,
                               rest=self.schema.rest,
                               version=self.schema.version,
                               restapi=self.schema.restApi,
                               rscpath=self.schema.resourcePath,
                               query=self.schema.query)
        return url

    @property
    def response(self):
        return self.locationApiData.text

    @property
    def response_to_json(self):
        return json.loads(self.locationApiData.text)

    @property
    def status_code(self):
        return self.locationApiData.status_code
