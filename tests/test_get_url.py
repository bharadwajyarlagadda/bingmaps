from bingmaps import BING_MAPS_KEY
from bingmaps.location import LocationByAddress
import os
import json
from collections import namedtuple
from .fixtures import (
    parametrie,
    create_tmp_dir
)

DATA = [{'queryParameters': {'adminDistrict': 'WA'}},
        {'key': 'vds'},
        {'queryParameters':
            {'adminDistrict': 'WA',
             'locality': 'Seattle',
             'key': 'abs'}},
        {'queryParameters':
            {'adminDistrict': 'FL',
             'locality': 'Miami',
             'key': BING_MAPS_KEY}},
        {'queryParameters':
            {'adminDistrict': 'WA',
             'locality': 'Seattle',
             'key': BING_MAPS_KEY}},
        {'queryParameters':
            {'adminDistrict': 'WA',
             'locality': 'Seattle',
             'o': 'xml',
             'key': BING_MAPS_KEY}},
        {'queryParameters':
            {'postalCode': 32310,
             'key': BING_MAPS_KEY
             }},
        {'queryParameters':
            {'adminDistrict': 'FL',
             'locality': 'Tallahassee',
             'key': BING_MAPS_KEY}},
        {'queryParameters':
            {'adminDistrict': 'TX',
             'key': BING_MAPS_KEY}},
        {'queryParameters':
            {'countryRegion': 'India',
             'key': BING_MAPS_KEY}},
        {'queryParameters':
            {'locality': 'Vijayawada',
             'key': BING_MAPS_KEY}},
        ]

expected_coordinates = namedtuple('expected', ['latitude', 'longitude'])


@parametrie('data', [
    (DATA[6]),
    (DATA[3]),
    (DATA[7]),
    (DATA[8]),
    (DATA[9]),
    (DATA[10])
])
def test_get_data_from_url(data):
    url = LocationByAddress(data)
    url.get_data()
    assert url.status_code == 200


@parametrie('data', [
    (DATA[3]),
    (DATA[4]),
    (DATA[6]),
    (DATA[7]),
    (DATA[8]),
    (DATA[9]),
    (DATA[10])
])
def test_create_json_file(create_tmp_dir, data):
    url = LocationByAddress(data)
    url.get_data()
    url.to_json_file(create_tmp_dir)
    with open(os.path.join(create_tmp_dir,
                           'locationByAddress.json'), 'r') as fp:
        assert len(json.load(fp)) > 0


@parametrie('data', [
    (DATA[4]),
    (DATA[3]),
    (DATA[6]),
    (DATA[7]),
    (DATA[8]),
    (DATA[9]),
    (DATA[10])
])
def test_get_coordinates(data):
    url = LocationByAddress(data)
    url.get_data()
    coordinates = url.get_coordinates
    assert len(coordinates) >= 1


@parametrie('data', [
    (DATA[3]),
    (DATA[4]),
    (DATA[6]),
    (DATA[7]),
    (DATA[8]),
    (DATA[9]),
    (DATA[10])
])
def test_get_address(data):
    url = LocationByAddress(data)
    url.get_data()
    addresses = url.get_address
    assert len(addresses) >= 1


@parametrie('data', [
    (DATA[3]),
    (DATA[4]),
    (DATA[6]),
    (DATA[7]),
    (DATA[8]),
    (DATA[9]),
    (DATA[10])
])
def test_get_bbox(data):
    url = LocationByAddress(data)
    url.get_data()
    bbox_list = url.get_bbox
    assert len(bbox_list) >= 1
