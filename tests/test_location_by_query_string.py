from bingmaps.urls import (
    LocationByQueryString,
    LocationByQuerySchema
)
from .fixtures import parametrize, BING_MAPS_KEY

DATA = [
    {'query': '1014 Oatney Ridge Ln., Morrisville, NC-27560',
     'key': BING_MAPS_KEY},
    {'query': '1014 Oatney Ridge Ln., Morrisville, NC-27560'},
    {'queryParameters': {
        'query': '1014 Oatney Ridge Ln., Morrisville, NC-27560',
        'key': BING_MAPS_KEY
    }}
]

EXPECTED = [
    False,
    True,
    'query=1014%20Oatney%20Ridge%20Ln.%2C%20Morrisville%2C%20NC-27560&'
    'includeNeighborhood=0&include=ciso2&maxResults=20&key={0}'.format(
        BING_MAPS_KEY
    ),
    {'version': 'v1', 'restApi': 'Locations', 'queryParameters':
     'query=1014%20Oatney%20Ridge%20Ln.%2C%20Morrisville%2C%20NC-27560&'
     'includeNeighborhood=0&include=ciso2&maxResults=20&key={0}'.format(
        BING_MAPS_KEY
     )}
]


@parametrize('data,expected', [
    (DATA[0], EXPECTED[0]),
    (DATA[1], EXPECTED[1])
])
def test_validate_location_by_query_string(data, expected):
    query = LocationByQueryString()
    is_valid_schema = query.validate(data)
    assert bool(is_valid_schema) == expected


@parametrize('data,expected', [
    (DATA[0], EXPECTED[2])
])
def test_location_by_query_query(data, expected):
    query = LocationByQueryString()
    query_string = query.dump(data).data
    assert query_string == expected


@parametrize('data,expected', [
    (DATA[2], EXPECTED[3])
])
def test_location_by_query_schema(data, expected):
    query_schema = LocationByQuerySchema()
    query_dict = query_schema.dump(data).data
    assert query_dict == expected
