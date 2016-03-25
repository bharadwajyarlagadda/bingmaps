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
        """Builds the URL for location API services based on the data given
        by the user.

        Returns:
            url (str): URL for the location API services
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
        """Returns response form the URL"""
        return self.locationApiData.text

    @property
    def status_code(self):
        """Returns status code from the URL response"""
        return self.locationApiData.status_code

    @property
    def get_coordinates(self):
        """Retrieves coordinates (latitudes/longitudes) from the output
        JSON/XML response

        Returns:
            coordinates (namedtuple): List of named tuples of coordinates
            (latitudes and longitudes)
        """
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
        """Retrieves addresses from the output JSON/XML response

        Returns:
            address (namedtuple): List of named tuples of addresses
        """
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
        """Retrieves the bounding box coordinates from the output JSON/XML
        response

        Returns:
            boundingbox (namedtuple): List of named tuples of bounding box
            coordinates
        """
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
        """Method to write response to a JSON file with the given file name"""
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
    """Location by address API class

    This class is used to retrieve the output from the given data from the
    user.
      - First, the data is used to build a URL which is related to the
        Locations by Address API.
      - Second, this class helps in retrieving the response from the URL built
      - Third, based on the response, this class helps in retrieving all the
        corresponding output data from the response. Some of the output data
        which this class would be retrieving is:
          - Coordinates (latitude/longitude)
          - BoundingBox coordinates (south latitude, west longitude,
            north latitude, east longitude)
          - Address

    The output from the URL can be either JSON/XML based on the output
    parameter mentioned in the data. Even the output response is 'xml', this
    class helps in converting the xml response to JSON data first and then
    retrieve all the necessary output from it.

    :ivar data: The data that the user will send in to the Location by address
        to retrieve all the respective output from the response
    :ivar url: The url that gets built based on the user's given data
    :ivar http_protocol: Http protocol for the URL. Can be either of the
        following:
          - http
          - https
    :ivar schema: The schema that gets used to build the URL and the schema
        is LocationByAddressUrl for location by address API service.
    :ivar file_name: The filename that the class can write the JSON response
        to.
          - file_name - 'locationByAddress'
    :ivar locationApiData: Response from the URL

    Some of the examples are illustrated in Examples page
    """
    def __init__(self, data, http_protocol='http'):
        if not bool(data):
            raise TypeError('No data given')
        schema = LocationByAddressUrl(data, httpprotocol=http_protocol)
        filename = 'locationByAddress'
        super().__init__(schema, filename, http_protocol)
        self.get_data()

    def get_data(self):
        """Gets data from the built url"""
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
    """Location by point API class

    This class is used to retrieve the output from the given data from the
    user.
      - First, the data is used to build a URL which is related to the
        Location by Point API.
      - Second, this class helps in retrieving the response from the URL built
      - Third, based on the response, this class helps in retrieving all the
        corresponding output data from the response. Some of the output data
        which this class would be retrieving is:
          - Coordinates (latitude/longitude)
          - BoundingBox coordinates (south latitude, west longitude,
            north latitude, east longitude)
          - Address

    The output from the URL can be either JSON/XML based on the output
    parameter mentioned in the data. Even the output response is 'xml', this
    class helps in converting the xml response to JSON data first and then
    retrieve all the necessary output from it.

    :ivar data: The data that the user will send in to the Location by point
        to retrieve all the respective output from the response
    :ivar url: The url that gets built based on the user's given data
    :ivar http_protocol: Http protocol for the URL. Can be either of the
        following:
          - http
          - https
    :ivar schema: The schema that gets used to build the URL and the schema
        is LocationByPointUrl for location by point API service.
    :ivar file_name: The filename that the class can write the JSON response
        to.
          - file_name - 'locationByPoint'
    :ivar locationApiData: Response from the URL

    Some of the examples are illustrated in Examples page
    """
    def __init__(self, data, http_protocol='http'):
        if not bool(data):
            raise TypeError('No data given')
        schema = LocationByPointUrl(data, httpprotocol=http_protocol)
        filename = 'locationByPoint'
        super().__init__(schema, filename, http_protocol)
        self.get_data()

    def get_data(self):
        """Gets data from the built url"""
        url = self.build_url()
        self.locationApiData = requests.get(url)
        if not self.locationApiData.status_code == 200:
            raise self.locationApiData.raise_for_status()

    def build_url(self):
        """Build the url and replaces /None/ with '/'"""
        url = super().build_url()
        if '/None/' in url:
            return url.replace('/None/', '/')
        else:
            return url


class LocationByQuery(LocationApi):
    """Location by query API class

    This class is used to retrieve the output from the given data from the
    user.
      - First, the data is used to build a URL which is related to the
        Location by Query API.
      - Second, this class helps in retrieving the response from the URL built
      - Third, based on the response, this class helps in retrieving all the
        corresponding output data from the response. Some of the output data
        which this class would be retrieving is:
          - Coordinates (latitude/longitude)
          - BoundingBox coordinates (south latitude, west longitude,
            north latitude, east longitude)
          - Address

    The output from the URL can be either JSON/XML based on the output
    parameter mentioned in the data. Even the output response is 'xml', this
    class helps in converting the xml response to JSON data first and then
    retrieve all the necessary output from it.

    :ivar data: The data that the user will send in to the Location by query
        to retrieve all the respective output from the response
    :ivar url: The url that gets built based on the user's given data
    :ivar http_protocol: Http protocol for the URL. Can be either of the
        following:
          - http
          - https
    :ivar schema: The schema that gets used to build the URL and the schema
        is LocationByQueryUrl for location by query API service.
    :ivar file_name: The filename that the class can write the JSON response
        to.
          - file_name - 'locationByQuery'
    :ivar locationApiData: Response from the URL

    Some of the examples are illustrated in Examples page
    """
    def __init__(self, data, http_protocol='http'):
        if not bool(data):
            raise TypeError('No data given')
        schema = LocationByQueryUrl(data, httpprotocol=http_protocol)
        filename = 'locationByQuery'
        super().__init__(schema, filename, http_protocol)
        self.get_data()

    def get_data(self):
        """Gets data from the built url"""
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
