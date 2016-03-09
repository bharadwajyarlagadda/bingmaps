import requests
from bingmaps.urlschema import LocationByPointUrl
from .location_api import LocationApi


class LocationByPoint(LocationApi):
    def __init__(self, data, http_protocol='http'):
        if not bool(data):
            raise TypeError('No data given')
        schema = LocationByPointUrl(data, protocol=http_protocol)
        super().__init__(schema, http_protocol)

    def get_data(self):
        """Gets data from the given url"""
        url = self.build_url()
        self.locationApiData = requests.get(url)

    def build_url(self):
        """Build the url and replaces /None/ with empty string"""
        url = super().build_url()
        if '/None/' in url:
            return url.replace('/None/', '/')
        else:
            return url
