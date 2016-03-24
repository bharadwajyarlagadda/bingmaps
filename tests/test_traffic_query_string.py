from .fixtures import parametrize
from bingmaps.urls import TrafficIncidentsSchema

DATA = [
    {'mapArea': [1, 2, 3, 4],
     'includeLocationCodes': 'true',
     'severity': [2, 4],
     'type': [2, 3],
     'key': 'abs'},
    {'includeLocationCodes': 'true',
     'severity': [2, 4],
     'type': [2, 3]}
]

EXPECTED = [
    ['v1', 'Traffic', 'Incidents',
     '1.0,2.0,3.0,4.0/true?severity=2,4&type=2,3&key=abs']
]


@parametrize('data,expected', [
    (DATA[0], EXPECTED[0])
])
def test_traffic_build_query_url(data, expected):
    traffic_data = TrafficIncidentsSchema()
    traffic_query = traffic_data.dump(data).data
    assert traffic_query['version'] in expected
    assert traffic_query['restApi'] in expected
    assert traffic_query['resourcePath'] in expected
    assert traffic_query['query'] in expected


@parametrize('data', [
    (DATA[1])
])
def test_validate_traffic_query_schema(data):
    traffic_data = TrafficIncidentsSchema()
    traffic_query = traffic_data.validate(data)
    assert 'mapArea' in traffic_query
    assert 'key' in traffic_query
