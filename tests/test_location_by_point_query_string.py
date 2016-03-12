from bingmaps.urls import (
    LocationByPointQueryString,
    LocationByPointSchema
)
from .fixtures import parametrize
from bingmaps import BING_MAPS_KEY


DATA = [
    {'point': '1,2',
     'includeEntityTypes': 'address',
     'key': BING_MAPS_KEY
     },
    {'point': '2,3',
     'includeEntityTypes': 'address',
     },
    {'queryParameters': {
        'point': '1,2',
        'includeEntityTypes': 'address',
        'key': BING_MAPS_KEY
    }}
]

EXPECTED = [
    '1,2?includeEntityTypes=address&includeNeighborhood=0&include=ciso2&key='
    '{0}'.format(BING_MAPS_KEY),
    True,
    False,
    {'version': 'v1', 'restApi': 'Locations', 'queryParameters':
        '1,2?includeEntityTypes=address&includeNeighborhood='
        '0&include=ciso2&key={0}'.format(BING_MAPS_KEY)}
]


@parametrize('data,expected', [
    (DATA[1], EXPECTED[1]),
    (DATA[0], EXPECTED[2])
])
def test_validate_location_by_point_query_string(data, expected):
    query = LocationByPointQueryString()
    is_valid_schema = query.validate(data)
    assert bool(is_valid_schema) == expected


@parametrize('data,expected', [
    (DATA[0], EXPECTED[0])
])
def test_location_by_point_query(data, expected):
    query = LocationByPointQueryString()
    query_string = query.dump(data).data
    assert query_string == expected


@parametrize('data,expected', [
    (DATA[2], EXPECTED[3])
])
def test_location_by_point_schema(data, expected):
    query_schema = LocationByPointSchema()
    query_dict = query_schema.dump(data).data
    assert query_dict == expected
