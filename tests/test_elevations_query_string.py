from .fixtures import BING_MAPS_KEY, parametrize
from bingmaps.urls import Coordinates, Polyline, Offset, BoundingBox

DATA = [
    {'method': 'List',
     'points': [15.5467, 34.5676],
     'key': BING_MAPS_KEY
     },
    {'key': BING_MAPS_KEY},
    {'method': 'List',
     'points': [15.5423, ],
     'key': BING_MAPS_KEY},
    {'method': 'Polyline',
     'points': [35.89431, -110.72522, 35.89393, -110.72578],
     'samples': 10,
     'key': BING_MAPS_KEY},
    {'key': BING_MAPS_KEY},
    {'method': 'Polyline',
     'points': [15.4356, ],
     'samples': 10,
     'key': BING_MAPS_KEY},
    {'method': 'SeaLevel',
     'points': [15.5467, 34.5676],
     'key': BING_MAPS_KEY
     },
    {'key': BING_MAPS_KEY},
    {'method': 'SeaLevel',
     'points': [15.5423, ],
     'key': BING_MAPS_KEY},
    {'method': 'Bounds',
     'bounds': [15.5463, 34.6577, 16.4365, 35.3245],
     'rows': 4,
     'cols': 5,
     'key': BING_MAPS_KEY},
    {'key': BING_MAPS_KEY},
    {'method': 'Bounds',
     'bounds': [15.5463, 34.6577, ],
     'rows': 4,
     'cols': 5,
     'key': BING_MAPS_KEY},
    {'method': 'Bounds',
     'bounds': [15.5463, 34.6577, 16.4365, 35.3245, 65.4356],
     'rows': 4,
     'cols': 5,
     'key': BING_MAPS_KEY},
]

EXPECTED = [
    'List?points=15.5467,34.5676&heights=sealevel&'
    'key={0}'.format(BING_MAPS_KEY),
    ['method', 'points'],
    ['points'],
    'Polyline?points=35.89431,-110.72522,35.89393,-110.72578&heights=sealevel&'
    'samples=10&key={0}'.format(BING_MAPS_KEY),
    ['method', 'points', 'samples'],
    ['points'],
    'SeaLevel?points=15.5467,34.5676&'
    'key={0}'.format(BING_MAPS_KEY),
    ['method', 'points'],
    ['points'],
    'Bounds?bounds=15.5463,34.6577,16.4365,35.3245&rows=4&'
    'cols=5&heights=sealevel&key={0}'.format(BING_MAPS_KEY),
    ['method', 'bounds', 'rows', 'cols'],
    ['bounds']
]


@parametrize('data,expected', [
    (DATA[0], EXPECTED[0])
])
def test_elevations_list_query_string(data, expected):
    elevations = Coordinates()
    elevations_query = elevations.dump(data).data
    assert elevations_query['query'] == expected


@parametrize('data,expected', [
    (DATA[1], EXPECTED[1]),
    (DATA[2], EXPECTED[2])
])
def test_validate_elevations_list(data, expected):
    elevations = Coordinates()
    is_valid_schema = elevations.validate(data)
    for expct in expected:
        assert expct in is_valid_schema


@parametrize('data,expected', [
    (DATA[3], EXPECTED[3])
])
def test_elevations_polyline_query_string(data, expected):
    polyline = Polyline()
    polyline_query = polyline.dump(data).data
    assert polyline_query['query'] == expected


@parametrize('data,expected', [
    (DATA[4], EXPECTED[4]),
    (DATA[5], EXPECTED[5])
])
def test_validate_elevations_polyline(data, expected):
    polyline = Polyline()
    is_valid_schema = polyline.validate(data)
    for expct in expected:
        assert expct in is_valid_schema


@parametrize('data,expected', [
    (DATA[6], EXPECTED[6])
])
def test_elevations_offset_query_string(data, expected):
    offset = Offset()
    offset_query = offset.dump(data).data
    assert offset_query['query'] == expected


@parametrize('data,expected', [
    (DATA[7], EXPECTED[7]),
    (DATA[8], EXPECTED[8])
])
def test_validate_elevations_offset(data, expected):
    offset = Offset()
    is_valid_schema = offset.validate(data)
    for expct in expected:
        assert expct in is_valid_schema


@parametrize('data,expected', [
    (DATA[9], EXPECTED[9])
])
def test_elevations_bounding_box_query_string(data, expected):
    bounding_box = BoundingBox()
    offset_query = bounding_box.dump(data).data
    assert offset_query['query'] == expected


@parametrize('data,expected', [
    (DATA[10], EXPECTED[10]),
    (DATA[11], EXPECTED[11]),
    (DATA[12], EXPECTED[11])
])
def test_validate_elevations_bounding_box(data, expected):
    bounding_box = BoundingBox()
    is_valid_schema = bounding_box.validate(data)
    for expct in expected:
        assert expct in is_valid_schema
