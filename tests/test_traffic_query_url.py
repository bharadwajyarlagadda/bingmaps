from .fixtures import parametrize, BING_MAPS_KEY
from bingmaps.apiservices import TrafficIncidentsApi


DATA = [
    {'mapArea': [16.5467, 26.4367, 17.4367, 27.4356],
     'includeLocationCodes': 'true',
     'severity': [2, 4],
     'type': [2, 3],
     'key': BING_MAPS_KEY}
]

EXPECTED = [
    'http://dev.virtualearth.net/REST/v1/Traffic/Incidents/16.5467,26.4367,'
    '17.4367,27.4356/true?severity=2,4&type=2,3&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Traffic/Incidents/16.5467,26.4367,'
    '17.4367,27.4356/true?severity=2,4&type=2,3&key={0}'.format(BING_MAPS_KEY)
]


@parametrize('data,expected', [
    (DATA[0], EXPECTED[0])
])
def test_traffic_incidents_build_url_http(data, expected):
    traffic_incidents = TrafficIncidentsApi(data)
    assert traffic_incidents.build_url() == expected


@parametrize('data,expected', [
    (DATA[0], EXPECTED[1])
])
def test_traffic_incidents_build_url_https(data, expected):
    traffic_incidents = TrafficIncidentsApi(data, http_protocol='https')
    assert traffic_incidents.build_url() == expected
