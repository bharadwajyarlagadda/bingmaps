from .fixtures import parametrize, https_protocol, create_tmp_dir
from bingmaps import BING_MAPS_KEY
import json
import os
from bingmaps.location import LocationByQuery

DATA = [
    {'queryParameters': {
        'query': '8672 Eagle Road Teaneck, NJ 07666',
        'key': BING_MAPS_KEY
    }},
    {'queryParameters': {
        'query': '7266 Canterbury Court Oshkosh, WI 54901',
        'key': BING_MAPS_KEY
    }},
    {'queryParameters': {
        'query': 'hyderabad',
        'o': 'xml',
        'c': 'te',
        'key': BING_MAPS_KEY
    }},
    {'queryParameters': {
        'query': 'Memphis',
        'o': 'xml',
        'c': 'te',
        'key': BING_MAPS_KEY
    }},
    {'queryParameters': {
        'query': '9106 Lakeview Drive Madison Heights, MI 48071',
        'key': BING_MAPS_KEY
    }},
    {'queryParameters': {
        'query': '4566 Clay Street Bolingbrook, IL 60440',
        'key': BING_MAPS_KEY
    }},
    {'queryParameters': {
        'query': '4856 Lawrence Street Burke, VA 22015',
        'key': BING_MAPS_KEY
    }},
]


@parametrize('data,expected', [
    (DATA[0], 200),
    (DATA[1], 200),
    (DATA[2], 200),
    (DATA[3], 200),
    (DATA[4], 200),
    (DATA[5], 200),
    (DATA[6], 200)
])
def test_location_by_query_url_get_data(data, expected):
    loc_by_query = LocationByQuery(data)
    assert loc_by_query.status_code == expected


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[2]),
    (DATA[3]),
    (DATA[4]),
    (DATA[5]),
    (DATA[6])
])
def test_create_json_file_location_by_query(create_tmp_dir, data):
    url = LocationByQuery(data, http_protocol=https_protocol)
    url.to_json_file(create_tmp_dir)
    with open(os.path.join(create_tmp_dir,
                           'locationByQuery.json'), 'r') as fp:
        assert len(json.load(fp)) > 0


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[2]),
    (DATA[3]),
    (DATA[4]),
    (DATA[5]),
    (DATA[6])
])
def test_location_by_query_get_coordinates(data):
    loc_by_point = LocationByQuery(data)
    assert len(loc_by_point.get_coordinates) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[2]),
    (DATA[3]),
    (DATA[4]),
    (DATA[5]),
    (DATA[6])
])
def test_location_by_query_get_addresses(data):
    loc_by_point = LocationByQuery(data)
    assert len(loc_by_point.get_address) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[2]),
    (DATA[3]),
    (DATA[4]),
    (DATA[5]),
    (DATA[6])
])
def test_location_by_query_get_bbox(data):
    loc_by_point = LocationByQuery(data)
    assert len(loc_by_point.get_bbox) >= 1
