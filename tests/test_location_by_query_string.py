from bingmaps.urls import LocationByQuerySchema
from .fixtures import parametrize, BING_MAPS_KEY

DATA = [
    {'q': '1014 Oatney Ridge Ln., Morrisville, NC-27560',
     'key': BING_MAPS_KEY},
    {'q': '1014 Oatney Ridge Ln., Morrisville, NC-27560'},
    {
        'q': '1014 Oatney Ridge Ln., Morrisville, NC-27560',
        'key': BING_MAPS_KEY
    }
]

EXPECTED = [
    False,
    True,
    'q=1014%20Oatney%20Ridge%20Ln.%2C%20Morrisville%2C%20NC-27560&'
    'includeNeighborhood=0&include=ciso2&maxResults=20&key={0}'.format(
        BING_MAPS_KEY
    ),
    {'version': 'v1', 'restApi': 'Locations', 'query':
     'q=1014%20Oatney%20Ridge%20Ln.%2C%20Morrisville%2C%20NC-27560&'
     'includeNeighborhood=0&include=ciso2&maxResults=20&key={0}'.format(
        BING_MAPS_KEY
     )}
]


@parametrize('data,expected', [
    (DATA[0], EXPECTED[0]),
    (DATA[1], EXPECTED[1])
])
def test_validate_location_by_query_string(data, expected):
    query = LocationByQuerySchema()
    is_valid_schema = query.validate(data)
    assert bool(is_valid_schema) == expected


@parametrize('data,expected', [
    (DATA[0], EXPECTED[2])
])
def test_location_by_query_query(data, expected):
    query = LocationByQuerySchema()
    query_string = query.dump(data).data
    assert query_string['query'] == expected


@parametrize('data,expected', [
    (DATA[2], EXPECTED[3])
])
def test_location_by_query_schema(data, expected):
    query_schema = LocationByQuerySchema()
    query_dict = query_schema.dump(data).data
    assert query_dict == expected
