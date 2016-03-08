import requests
from bingmaps.urlschema import LocationByAddressUrl
import os
import json
from collections import namedtuple


class LocationByAddress(object):
    def __init__(self, data, http_protocol='http'):
        if bool(data):
            self.data = data
        else:
            raise TypeError('No data given')
        self.http_protocol = http_protocol
        self.file_name = 'locationByAddress'
        self.locationByAddressData = None

    def get_data(self):
        url = self.build_url(self.data, self.http_protocol)
        self.locationByAddressData = requests.get(url)

    def build_url(self, data, protocol):
        schema = LocationByAddressUrl(data, protocol)
        url = '{protocol}/{url}/{rest}/{version}/{restapi}/{rscpath}/' \
              '{query}'.format(protocol=schema.protocol,
                               url=schema.main_url,
                               rest=schema.rest,
                               version=schema.version,
                               restapi=schema.restApi,
                               rscpath=schema.resourcePath,
                               query=schema.query)
        if '//?' in url:
            return url.replace('//?', '?')
        else:
            return url

    @property
    def response(self):
        return self.locationByAddressData.text

    @property
    def response_to_json(self):
        return json.loads(self.locationByAddressData.text)

    @property
    def status_code(self):
        return self.locationByAddressData.status_code

    def get_resource(self):
        try:
            resourceSets = self.response_to_json['resourceSets']
            for resource in resourceSets:
                return [rsc for rsc in resource['resources']]
        except KeyError:
            print(KeyError)

    @property
    def get_coordinates(self):
        """Write output schema for this"""
        resource_list = self.get_resource()
        coordinates_list = []
        coordinates = namedtuple('coordinates', ['latitude', 'longitude'])
        try:
            for resource in resource_list:
                if 'point' in resource:
                    coordinates_list.append(
                        coordinates(*resource['point']['coordinates'])
                    )
            return coordinates_list
        except KeyError:
            print(KeyError)

    @property
    def get_address(self):
        resource_list = self.get_resource()
        address_list = []
        try:
            for resource in resource_list:
                if 'address' in resource:
                    address_list.append(resource['address'])
            return address_list
        except KeyError:
            print(KeyError)

    @property
    def get_bbox(self):
        resource_list = self.get_resource()
        bounding_box = namedtuple('boundingBox', ['SouthLatitude',
                                                  'WestLongitude',
                                                  'NorthLatitude',
                                                  'EastLongitude'])
        bounding_box_list = []
        try:
            for resource in resource_list:
                if 'bbox' in resource:
                    bounding_box_list.append(bounding_box(*resource['bbox']))
            return bounding_box_list
        except KeyError:
            print(KeyError)

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

    def to_xml(self):
        pass

    def to_csv(self):
        pass
