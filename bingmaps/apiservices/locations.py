import json
import os
import requests
from collections import namedtuple
import xmltodict
from bingmaps.urls import (
    LocationByAddressUrl,
    LocationByQueryUrl,
    LocationByPointUrl
)


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
            resourceSets = self.response_to_dict()['resourceSets']
            for resource in resourceSets:
                return [rsc for rsc in resource['resources']]
        except KeyError:
            try:
                response = self.response_to_dict()['Response']
                resourceSets = response['ResourceSets']
                location = resourceSets['ResourceSet']['Resources']['Location']
                return location
            except KeyError:
                print(KeyError)

    def response_to_dict(self):
        try:
            return json.loads(self.locationApiData.text)
        except Exception:
            return json.loads(json.dumps(xmltodict.parse(
                self.locationApiData.text)))

    @property
    def response(self):
        return self.locationApiData.text

    @property
    def status_code(self):
        return self.locationApiData.status_code

    @property
    def get_coordinates(self):
        """Write output schema for this"""
        resource_list = self.get_resource()
        coordinates = namedtuple('coordinates', ['latitude', 'longitude'])
        try:
            return [coordinates(*resource['point']['coordinates'])
                    for resource in resource_list]
        except (KeyError, TypeError):
            try:
                if isinstance(resource_list, dict):
                    resource_list = [resource_list]
                return [coordinates(resource['Point']['Latitude'],
                                    resource['Point']['Longitude'])
                        for resource in resource_list]
            except (KeyError, ValueError) as exc:
                print(exc)

    @property
    def get_address(self):
        resource_list = self.get_resource()
        try:
            return [resource['address'] for resource in resource_list]
        except (KeyError, TypeError):
            try:
                if isinstance(resource_list, dict):
                    resource_list = [resource_list]
                return [resource['Address'] for resource in resource_list]
            except (KeyError, TypeError) as exc:
                print(exc)

    @property
    def get_bbox(self):
        resource_list = self.get_resource()
        bounding_box = namedtuple('boundingbox', ['southlatitude',
                                                  'westlongitude',
                                                  'northlatitude',
                                                  'eastlongitude'])
        try:
            return [bounding_box(*resource['bbox'])
                    for resource in resource_list]
        except (KeyError, TypeError):
            try:
                if isinstance(resource_list, dict):
                    resource_list = [resource_list]
                return [bounding_box(resource['BoundingBox']['SouthLatitude'],
                                     resource['BoundingBox']['WestLongitude'],
                                     resource['BoundingBox']['NorthLatitude'],
                                     resource['BoundingBox']['EastLongitude'])
                        for resource in resource_list]
            except (KeyError, TypeError) as exc:
                print(exc)

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
            json.dump(self.response, fp)


class LocationByAddress(LocationApi):
    def __init__(self, data, http_protocol='http'):
        if not bool(data):
            raise TypeError('No data given')
        schema = LocationByAddressUrl(data, httpprotocol=http_protocol)
        filename = 'locationByAddress'
        super().__init__(schema, filename, http_protocol)
        self.get_data()

    def get_data(self):
        """Gets data from the given url"""
        url = self.build_url()
        self.locationApiData = requests.get(url)
        if not self.locationApiData.status_code == 200:
            raise self.locationApiData.raise_for_status()

    def build_url(self):
        """Build the url and replaces /None/ with empty string"""
        url = super().build_url()
        if '/None/' in url:
            return url.replace('/None/', '')
        else:
            return url


class LocationByPoint(LocationApi):
    def __init__(self, data, http_protocol='http'):
        if not bool(data):
            raise TypeError('No data given')
        schema = LocationByPointUrl(data, httpprotocol=http_protocol)
        filename = 'locationByPoint'
        super().__init__(schema, filename, http_protocol)
        self.get_data()

    def get_data(self):
        """Gets data from the given url"""
        url = self.build_url()
        self.locationApiData = requests.get(url)
        if not self.locationApiData.status_code == 200:
            raise self.locationApiData.raise_for_status()

    def build_url(self):
        """Build the url and replaces /None/ with empty string"""
        url = super().build_url()
        if '/None/' in url:
            return url.replace('/None/', '/')
        else:
            return url


class LocationByQuery(LocationApi):
    def __init__(self, data, http_protocol='http'):
        if not bool(data):
            raise TypeError('No data given')
        schema = LocationByQueryUrl(data, httpprotocol=http_protocol)
        filename = 'locationByQuery'
        super().__init__(schema, filename, http_protocol)
        self.get_data()

    def get_data(self):
        url = self.build_url()
        self.locationApiData = requests.get(url)
        if not self.locationApiData.status_code == 200:
            raise self.locationApiData.raise_for_status()

    def build_url(self):
        url = super().build_url()
        if '/None/' in url:
            return url.replace('/None/', '')
        else:
            return url
