from bingmaps.apiservices import TrafficIncidentsApi
from .fixtures import BING_MAPS_KEY, parametrize


DATA = [
    {'mapArea': [37, -105, 45, -94],
     'includeLocationCodes': 'true',
     'key': BING_MAPS_KEY},
    {'mapArea': [37, -105, 45, -94],
     'includeLocationCodes': 'true',
     'type': [5],
     'o': 'xml',
     'key': BING_MAPS_KEY},
    {'mapArea': [45.219, -122.325, 47.610, -122.107],
     'includeLocationCodes': 'true',
     'severity': [2, 4],
     'type': [2, 3],
     'o': 'xml',
     'key': BING_MAPS_KEY}
]


@parametrize('data', [
    (DATA[0])
])
def test_status_code(data):
    incidents = TrafficIncidentsApi(data)
    assert incidents.status_code == 200


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def test_get_resource(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.get_resource()) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def test_get_coordinates(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.get_coordinates) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def test_get_traffic_incident(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.traffic_incident()) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_description(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.description) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_congestion(data):
    incidents = TrafficIncidentsApi(data)
    assert incidents.congestion is None


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_detour(data):
    incidents = TrafficIncidentsApi(data)
    assert incidents.detour_info is None


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_start_time(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.start_time) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_end_time(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.end_time) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_incident_id(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.incident_id) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_lane_info(data):
    incidents = TrafficIncidentsApi(data)
    assert incidents.lane_info is None


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_last_modified(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.last_modified) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_road_closed(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.road_closed) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_severity(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.severity) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_type(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.type) >= 1


@parametrize('data', [
    (DATA[0]),
    (DATA[1])
])
def tests_get_verification(data):
    incidents = TrafficIncidentsApi(data)
    assert len(incidents.is_verified) >= 1


@parametrize('data', [
    (DATA[2])
])
def test_get_resource_none(data):
    incidents = TrafficIncidentsApi(data)
    assert incidents.get_resource()[0] is None
