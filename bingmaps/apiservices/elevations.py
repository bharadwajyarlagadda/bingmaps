from bingmaps.urls import (
    ElevationsUrl,
    CoordinatesSchema,
    OffsetSchema,
    PolylineSchema,
    BoundingBoxSchema
)
from collections import namedtuple
import requests
import json
import os
import xmltodict


class ElevationsApi(object):
    def __init__(self, data, http_protocol='http'):
        self.http_protocol = http_protocol
        schema = None
        if not bool(data):
            raise TypeError('No data given')
        if data['queryParameters']['method'] == 'List':
            schema = CoordinatesSchema()
        elif data['queryParameters']['method'] == 'Polyline':
            schema = PolylineSchema()
        elif data['queryParameters']['method'] == 'SeaLevel':
            schema = OffsetSchema()
        elif data['queryParameters']['method'] == 'Bounds':
            schema = BoundingBoxSchema()
        self.schema = ElevationsUrl(data, http_protocol, schema)
        self.file_name = 'elevations'
        self.elevationdata = None
        self.get_data()

    def build_url(self):
        url = '{protocol}/{url}/{rest}/{version}/{restapi}/{rscpath}/' \
              '{query}'.format(protocol=self.schema.protocol,
                               url=self.schema.main_url,
                               rest=self.schema.rest,
                               version=self.schema.version,
                               restapi=self.schema.restApi,
                               rscpath=self.schema.resourcePath,
                               query=self.schema.query)
        return url.replace('/None/', '/')

    def get_data(self):
        """Gets data from the given url"""
        url = self.build_url()
        self.elevationdata = requests.get(url)
        if not self.elevationdata.status_code == 200:
            raise self.elevationdata.raise_for_status()

    def get_resource(self):
        resourceSets = self.response_to_dict()
        try:
            for resource in resourceSets['resourceSets']:
                return [rsc for rsc in resource['resources']]
        except KeyError:
            try:
                resourcesSets = resourceSets['Response']['ResourceSets']
                resourceSet = resourcesSets['ResourceSet']
                if isinstance(resourceSet, dict):
                    return resourceSet['Resources']
                elif isinstance((resourceSet, list)):
                    return [rsc for rsc in resourceSet['Resources']]
            except KeyError:
                print(KeyError)

    @property
    def response(self):
        return self.elevationdata.text

    @property
    def status_code(self):
        return self.elevationdata.status_code

    def response_to_dict(self):
        try:
            return json.loads(self.elevationdata.text)
        except Exception:
            return json.loads(json.dumps(xmltodict.parse(
                self.elevationdata.text)))

    @property
    def elevations(self):
        resources = self.get_resource()
        elevations = namedtuple('elevations_data', 'elevations')
        try:
            return [elevations(resource['elevations'])
                    for resource in resources]
        except KeyError:
            return [elevations(resource['offsets'])
                    for resource in resources]
        except TypeError:
            try:
                if isinstance(resources['ElevationData']['Elevations'], dict):
                    return elevations(resources['ElevationData']['Elevations'])
            except KeyError:
                offsets = namedtuple('offsets_data', 'offsets')
                try:
                    if isinstance(resources['SeaLevelData']['Offsets'], dict):
                        return offsets(resources['SeaLevelData']['Offsets'])
                except KeyError:
                    print(KeyError)

    @property
    def zoomlevel(self):
        resources = self.get_resource()
        zoomlevel = namedtuple('zoomlevel', 'zoomLevel')
        try:
            return [zoomlevel(resource['zoomLevel'])
                    for resource in resources]
        except TypeError:
            try:
                if isinstance(resources['ElevationData'], dict):
                    return zoomlevel(resources['ElevationData']['ZoomLevel'])
            except KeyError:
                try:
                    if isinstance(resources['SeaLevelData'], dict):
                        zoom = resources['SeaLevelData']['ZoomLevel']
                        return zoomlevel(zoom)
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
            json.dump(self.response, fp)
