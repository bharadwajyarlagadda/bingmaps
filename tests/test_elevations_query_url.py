from .fixtures import BING_MAPS_KEY, parametrize
from bingmaps.apiservices import ElevationsApi

DATA = [
    {'method': 'List',
     'points': [15.5467, 34.5676],
     'key': BING_MAPS_KEY
     },
    {'method': 'Polyline',
     'points': [35.89431, -110.72522, 35.89393, -110.72578],
     'samples': 10,
     'key': BING_MAPS_KEY},
    {'method': 'SeaLevel',
     'points': [15.5467, 34.5676],
     'key': BING_MAPS_KEY
     },
    {'method': 'Bounds',
     'bounds': [15.5463, 34.6577, 16.4365, 35.3245],
     'rows': 4,
     'cols': 5,
     'key': BING_MAPS_KEY}
]

EXPECTED = [
    'http://dev.virtualearth.net/REST/v1/Elevation/List?'
    'points=15.5467,34.5676&heights=sealevel&'
    'key={0}'.format(BING_MAPS_KEY),
    'http://dev.virtualearth.net/REST/v1/Elevation/Polyline?'
    'points=35.89431,-110.72522,35.89393,-110.72578&heights=sealevel&'
    'samples=10&key={0}'.format(BING_MAPS_KEY),
    'http://dev.virtualearth.net/REST/v1/Elevation/SeaLevel?'
    'points=15.5467,34.5676&'
    'key={0}'.format(BING_MAPS_KEY),
    'http://dev.virtualearth.net/REST/v1/Elevation/Bounds?'
    'bounds=15.5463,34.6577,16.4365,35.3245&rows=4&'
    'cols=5&heights=sealevel&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Elevation/List?'
    'points=15.5467,34.5676&heights=sealevel&'
    'key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Elevation/Polyline?'
    'points=35.89431,-110.72522,35.89393,-110.72578&heights=sealevel&'
    'samples=10&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Elevation/SeaLevel?'
    'points=15.5467,34.5676&'
    'key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Elevation/Bounds?'
    'bounds=15.5463,34.6577,16.4365,35.3245&rows=4&'
    'cols=5&heights=sealevel&key={0}'.format(BING_MAPS_KEY),
]


@parametrize('data,expected', [
    (DATA[0], EXPECTED[0]),
    (DATA[1], EXPECTED[1]),
    (DATA[2], EXPECTED[2]),
    (DATA[3], EXPECTED[3])
])
def test_elevations_query_url_http(data, expected):
    elevations_url = ElevationsApi(data)
    assert elevations_url.build_url() == expected


@parametrize('data,expected', [
    (DATA[0], EXPECTED[4]),
    (DATA[1], EXPECTED[5]),
    (DATA[2], EXPECTED[6]),
    (DATA[3], EXPECTED[7])
])
def test_elevations_query_url_https(data, expected):
    elevations_url = ElevationsApi(data, 'https')
    assert elevations_url.build_url() == expected
