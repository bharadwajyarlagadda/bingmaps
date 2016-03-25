from .fixtures import (
    parametrize,
    create_tmp_dir,
    https_protocol,
    BING_MAPS_KEY
)
import json
import os
from bingmaps.apiservices import LocationByPoint

DATA = [
    {
        'point': '16.506174,80.648015',
        'includeEntityTypes': 'address',
        'key': BING_MAPS_KEY
    },
    {
        'point': '30.438256,-84.280733',
        'includeEntityTypes': 'Neighborhood',
        'key': BING_MAPS_KEY
    },
    {
        'point': '35.689487,139.691706',
        'includeEntityTypes': 'PopulatedPlace',
        'key': BING_MAPS_KEY
    },
    {
        'point': '39.904211,116.407395',
        'includeEntityTypes': 'Postcode1',
        'key': BING_MAPS_KEY
    },
    {
        'point': '12.971599,77.594563',
        'includeEntityTypes': 'AdminDivision1',
        'c': 'te',
        'key': BING_MAPS_KEY
    },
    {
        'point': '28.613939,77.209021',
        'includeEntityTypes': 'AdminDivision2',
        'key': BING_MAPS_KEY
    },
    {
        'point': '26.449923,80.331874',
        'includeEntityTypes': 'CountryRegion',
        'key': BING_MAPS_KEY
    },
    {
        'point': '26.449923,80.331874',
        'o': 'xml',
        'includeEntityTypes': 'CountryRegion',
        'key': BING_MAPS_KEY
    },
]


@parametrize('data,expected', [
    (DATA[0], 200),
    (DATA[1], 200),
    (DATA[2], 200),
    (DATA[3], 200),
    (DATA[4], 200),
    (DATA[5], 200),
    (DATA[6], 200),
    (DATA[7], 200)
])
def test_location_by_point_url_get_data(data, expected):
    loc_by_point = LocationByPoint(data)
    assert loc_by_point.status_code == expected


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[2]),
    (DATA[3]),
    (DATA[4]),
    (DATA[5]),
    (DATA[6]),
    (DATA[7])
])
def test_create_json_file_location_by_point(create_tmp_dir, data):
    url = LocationByPoint(data, http_protocol=https_protocol)
    url.to_json_file(create_tmp_dir)
    with open(os.path.join(create_tmp_dir,
                           'locationByPoint.json'), 'r') as fp:
        assert len(json.load(fp)) > 0


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[2]),
    (DATA[4]),
    (DATA[5]),
    (DATA[6]),
    (DATA[7])
])
def test_location_by_point_get_coordinates(data):
    loc_by_point = LocationByPoint(data)
    assert len(loc_by_point.get_coordinates) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[2]),
    (DATA[4]),
    (DATA[5]),
    (DATA[6]),
    (DATA[7])
])
def test_location_by_point_get_addresses(data):
    loc_by_point = LocationByPoint(data)
    assert len(loc_by_point.get_address) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[2]),
    (DATA[4]),
    (DATA[5]),
    (DATA[6]),
    (DATA[7])
])
def test_location_by_point_get_bbox(data):
    loc_by_point = LocationByPoint(data)
    assert len(loc_by_point.get_bbox) >= 1


@parametrize('data', [
    (DATA[3])
])
def test_location_by_point_postcode1(data):
    loc_by_point = LocationByPoint(data)
    assert bool(loc_by_point.response) is True
    assert len(loc_by_point.get_coordinates) == 0
    assert len(loc_by_point.get_address) == 0
    assert len(loc_by_point.get_bbox) == 0
