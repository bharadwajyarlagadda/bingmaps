import requests
from bingmaps.urlschema import LocationByQueryUrl
from .location_api import LocationApi


class LocationByQuery(LocationApi):
    def __init__(self, data, http_protocol='http'):
        if not bool(data):
            raise TypeError('No data given')
        schema = LocationByQueryUrl(data, protocol=http_protocol)
        filename = 'locationByQuery'
        super().__init__(schema, filename, http_protocol)
        self.get_data()

    def get_data(self):
        url = self.build_url()
        self.locationApiData = requests.get(url)

    def build_url(self):
        url = super().build_url()
        if '/None/' in url:
            return url.replace('/None/', '')
        else:
            return url
