import requests
from bingmaps.utils import UrlProps


class LocationByAddress(object):
    def __init__(self, data, http_protocol='http'):
        self.data = data
        self.http_protocol = http_protocol

    def get_data(self):
        url = self.build_url(self.data, self.http_protocol)
        data = requests.get(url)
        return data

    def build_url(self, data, protocol):
        schema = UrlProps(data, protocol)
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
