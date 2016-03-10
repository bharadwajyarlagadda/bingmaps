import json
import os
from collections import namedtuple


class LocationApi(object):
    """Parent class for LocationByAddress and LocationByPoint api classes"""
    def __init__(self, schema, filename, http_protocol='http'):
        self.http_protocol = http_protocol
        self.file_name = filename
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

    def get_resource(self):
        try:
            resourceSets = self.response_to_json['resourceSets']
            for resource in resourceSets:
                return [rsc for rsc in resource['resources']]
        except KeyError:
            print(KeyError)

    @property
    def response(self):
        return self.locationApiData.text

    @property
    def response_to_json(self):
        return json.loads(self.locationApiData.text)

    @property
    def status_code(self):
        return self.locationApiData.status_code

    @property
    def get_coordinates(self):
        """Write output schema for this"""
        resource_list = self.get_resource()
        coordinates = namedtuple('coordinates', ['latitude', 'longitude'])
        return [coordinates(*resource['point']['coordinates'])
                for resource in resource_list]

    @property
    def get_address(self):
        resource_list = self.get_resource()
        return [resource['address'] for resource in resource_list]

    @property
    def get_bbox(self):
        resource_list = self.get_resource()
        bounding_box = namedtuple('boundingBox', ['SouthLatitude',
                                                  'WestLongitude',
                                                  'NorthLatitude',
                                                  'EastLongitude'])
        return [bounding_box(*resource['bbox']) for resource in resource_list]

    def to_json_file(self, path, file_name=None):
        if bool(path) and os.path.isdir(path):
            self.write_to_json(path, file_name)
        else:
            self.write_to_json(os.getcwd(), file_name)

    def write_to_json(self, path, file_name):
        if file_name is None:
            file_name = self.file_name
        with open(os.path.join(path,
                               '{0}.{1}'.format(file_name,
                                                'json')), 'w') as fp:
            json.dump(self.response_to_json, fp)
