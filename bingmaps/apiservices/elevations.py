from bingmaps.urls import (
    ElevationsUrl,
    Coordinates,
    Offset,
    Polyline,
    BoundingBox
)
from collections import namedtuple
import requests
import json
import os
import xmltodict


class ElevationsApi(object):
    """Elevations API class

    This class is used to retrieve the output from the given data from the
    user.
      - First, the data is used to build a URL which is related to the
        Elevations API.
      - Second, this class helps in retrieving the response from the URL built
      - Third, based on the response, this class helps in retrieving all the
        corresponding output data from the response. Some of the output data
        which this class would be retrieving is:
          - Elevations
          - Offsets
          - Zoom Level

    The output from the URL can be either JSON/XML based on the output
    parameter mentioned in the data. Even the output response is 'xml', this
    class helps in converting the xml response to JSON data first and then
    retrieve all the necessary output from it.

    :ivar data: The data that the user will send in to the ElevationsApi to
        retrieve all the respective output from the response
    :ivar url: The url that gets built based on the user's given data
    :ivar http_protocol: Http protocol for the URL. Can be either of the
        following:
          - http
          - https
    :ivar schema: The schema that gets used to build the URL and the schema
        is based in the 'method' field in the data.
    :ivar file_name: The filename that the class can write the JSON response
        to.
          - file_name - 'elevations'
    :ivar elevationdata: Response from the URL

    Some of the examples are illustrated in Examples page
    """
    def __init__(self, data, http_protocol='http'):
        self.http_protocol = http_protocol
        if not bool(data):
            raise TypeError('No data given')
        if data['method'] == 'List':
            schema = Coordinates()
        elif data['method'] == 'Polyline':
            schema = Polyline()
        elif data['method'] == 'SeaLevel':
            schema = Offset()
        elif data['method'] == 'Bounds':
            schema = BoundingBox()
        else:
            raise KeyError('method should be either of '
                           'List/Polyline/SeaLevel/Bounds')

        self.schema = ElevationsUrl(data, http_protocol, schema)
        self.file_name = 'elevations'
        self.elevationdata = None
        self.get_data()

    def build_url(self):
        """Builds the URL for elevations API services based on the data given
        by the user.

        Returns:
            url (str): URL for the elevations API services
        """
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
                elif isinstance(resourceSet, list):
                    return [rsc for rsc in resourceSet['Resources']]
            except KeyError:
                print(KeyError)

    @property
    def response(self):
        """Response from the built URL"""
        return self.elevationdata.text

    @property
    def status_code(self):
        """Status code of the response from the URL"""
        return self.elevationdata.status_code

    def response_to_dict(self):
        """This method helps in returning the output JSON data from the URL
        and also it helps in converting the XML output/response (string) to a
        JSON object

        Returns:
            data (dict): JSON data from the output/response
        """
        try:
            return json.loads(self.elevationdata.text)
        except Exception:
            return json.loads(json.dumps(xmltodict.parse(
                self.elevationdata.text)))

    @property
    def elevations(self):
        """Retrieves elevations/offsets from the output response

        Returns:
            elevations/offsets (namedtuple): A named tuple of list of
            elevations/offsets
        """
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
        """Retrieves zoomlevel from the output response

        Returns:
            zoomlevel (namedtuple): A namedtuple of zoomlevel from the output
            response
        """
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
        """Writes output to a JSON file with the given file name"""
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
