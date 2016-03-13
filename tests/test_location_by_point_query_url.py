from bingmaps.apiservices import LocationByPoint
from bingmaps import BING_MAPS_KEY
from .fixtures import parametrize, https_protocol

DATA = [
    {'queryParameters': {
        'point': '1,2',
        'includeEntityTypes': 'address',
        'key': BING_MAPS_KEY}},
    {'queryParameters': {
        'point': '3,4',
        'includeEntityTypes': 'Neighborhood',
        'key': BING_MAPS_KEY}},
    {'queryParameters': {
        'point': '5,6',
        'includeEntityTypes': 'PopulatedPlace',
        'key': BING_MAPS_KEY}},
    {'queryParameters': {
        'point': '9,10',
        'includeEntityTypes': 'Postcode1',
        'key': BING_MAPS_KEY}},
    {'queryParameters': {
        'point': '1,2',
        'includeEntityTypes': 'AdminDivision1',
        'key': BING_MAPS_KEY}},
    {'queryParameters': {
        'point': '1,2',
        'includeEntityTypes': 'AdminDivision2',
        'key': BING_MAPS_KEY}},
    {'queryParameters': {
        'point': '1,2',
        'includeEntityTypes': 'CountryRegion',
        'key': BING_MAPS_KEY}},
]

EXPECTED = [
    'http://dev.virtualearth.net/REST/v1/Locations/1,2?includeEntityTypes='
    'address&includeNeighborhood=0&include='
    'ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
    'http://dev.virtualearth.net/REST/v1/Locations/3,4?includeEntityTypes='
    'Neighborhood&includeNeighborhood=0&include='
    'ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
    'http://dev.virtualearth.net/REST/v1/Locations/5,6?includeEntityTypes='
    'PopulatedPlace&includeNeighborhood=0&include='
    'ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
    'http://dev.virtualearth.net/REST/v1/Locations/9,10?includeEntityTypes='
    'Postcode1&includeNeighborhood=0&include='
    'ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Locations/1,2?includeEntityTypes='
    'AdminDivision1&includeNeighborhood=0&include='
    'ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Locations/1,2?includeEntityTypes='
    'AdminDivision2&includeNeighborhood=0&include='
    'ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Locations/1,2?includeEntityTypes='
    'CountryRegion&includeNeighborhood=0&include='
    'ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
]


@parametrize('data,expected', [
    (DATA[0], EXPECTED[0]),
    (DATA[1], EXPECTED[1]),
    (DATA[2], EXPECTED[2]),
    (DATA[3], EXPECTED[3])
])
def test_location_by_point_url_http_protocol(data, expected):
    loc_by_point = LocationByPoint(data)
    assert loc_by_point.build_url() == expected


@parametrize('data,expected', [
    (DATA[4], EXPECTED[4]),
    (DATA[5], EXPECTED[5]),
    (DATA[6], EXPECTED[6])
])
def test_location_by_point_url_https_protocol(data, expected):
    loc_by_point = LocationByPoint(data, https_protocol)
    assert loc_by_point.build_url() == expected
