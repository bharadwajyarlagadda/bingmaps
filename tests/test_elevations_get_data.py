from .fixtures import BING_MAPS_KEY, parametrize
from bingmaps.apiservices import ElevationsApi
import os
import json

DATA = [
    {'queryParameters': {'method': 'List',
     'points': [15.5467, 34.5676],
     'key': BING_MAPS_KEY
     }},
    {'queryParameters': {'method': 'Polyline',
     'points': [35.89431, -110.72522, 35.89393, -110.72578],
     'samples': 10,
     'key': BING_MAPS_KEY}},
    {'queryParameters': {'method': 'SeaLevel',
     'points': [15.5467, 34.5676],
     'key': BING_MAPS_KEY
     }},
    {'queryParameters': {'method': 'Bounds',
     'bounds': [15.5463, 34.6577, 16.4365, 35.3245],
     'rows': 4,
     'cols': 5,
     'key': BING_MAPS_KEY}},
    {'queryParameters': {'method': 'List',
     'points': [15.5467, 34.5676],
     'o': 'xml',
     'key': BING_MAPS_KEY
     }},
    {'queryParameters': {'method': 'Polyline',
     'points': [35.89431, -110.72522, 35.89393, -110.72578],
     'samples': 10,
     'o': 'xml',
     'key': BING_MAPS_KEY}},
    {'queryParameters': {'method': 'SeaLevel',
     'points': [15.5467, 34.5676],
     'o': 'xml',
     'key': BING_MAPS_KEY
     }},
    {'queryParameters': {'method': 'Bounds',
     'bounds': [15.5463, 34.6577, 16.4365, 35.3245],
     'rows': 4,
     'cols': 5,
     'o': 'xml',
     'key': BING_MAPS_KEY}},
]


@parametrize('data,expected', [
    (DATA[0], 200),
    (DATA[1], 200),
    (DATA[2], 200),
    (DATA[3], 200)
])
def test_elevations_status_code(data, expected):
    elevations = ElevationsApi(data)
    assert elevations.status_code == expected


@parametrize('data', [
    (DATA[4]),
    (DATA[5]),
    (DATA[6]),
    (DATA[7])
])
def test_elevations_status_code_xml(data):
    elevations = ElevationsApi(data)
    assert len(elevations.get_resource()) >= 1


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
def test_elevations_elevations_xml(data):
    elevations = ElevationsApi(data)
    assert len(elevations.elevations) >= 1


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
def test_elevations_zoom_level_xml(data):
    elevations = ElevationsApi(data)
    assert len(elevations.zoomlevel) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[2]),
    (DATA[3])
])
def test_create_json_file_elevations(create_tmp_dir, data):
    url = ElevationsApi(data)
    url.to_json_file(create_tmp_dir)
    with open(os.path.join(create_tmp_dir,
                           'elevations.json'), 'r') as fp:
        assert len(json.load(fp)) > 0


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
def test_elevations_response(data):
    elevations = ElevationsApi(data)
    assert bool(elevations.response) is True


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[3])
])
def test_elevations_elevations_https(data):
    elevations = ElevationsApi(data, 'https')
    assert len(elevations.elevations) >= 1


@parametrize('data', [
    (DATA[2])
])
def test_elevations_offsets_https(data):
    elevations = ElevationsApi(data, 'https')
    assert len(elevations.elevations) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1]),
    (DATA[2]),
    (DATA[3])
])
def test_elevations_zoom_level_https(data):
    elevations = ElevationsApi(data, 'https')
    assert len(elevations.zoomlevel) >= 1
