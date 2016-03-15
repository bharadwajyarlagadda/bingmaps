import pytest

from bingmaps.apiservices import LocationByAddress
from bingmaps.urls import LocationByAddressQueryString
from .fixtures import parametrize, BING_MAPS_KEY

http_protocol = 'http'
https_protocol = 'https'

DATA = [{'queryParameters': {'adminDistrict': 'WA'}},
        {'key': 'vds'},
        {'queryParameters':
            {'adminDistrict': 'WA',
             'locality': 'Seattle',
             'key': 'abs'}},
        {'queryParameters':
            {'adminDistrict': 'WA',
             'locality': 'Seattle',
             'key': BING_MAPS_KEY}},
        {'queryParameters':
            {'adminDistrict': 'WA',
             'locality': 'Seattle',
             'key': BING_MAPS_KEY}},
        {'queryParameters':
            {'adminDistrict': 'WA',
             'locality': 'Seattle',
             'o': 'xml',
             'key': BING_MAPS_KEY}}
        ]

EXPECTED = [
    True,
    False,
    'adminDistrict=WA&locality=Seattle&includeNeighborhood='
    '0&include=ciso2&maxResults=20&key=abs',
    'http://dev.virtualearth.net/REST/v1/Locations?'
    'adminDistrict=WA&locality=Seattle&includeNeighborhood='
    '0&include=ciso2&maxResults='
    '20&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Locations?'
    'adminDistrict=WA&locality=Seattle&includeNeighborhood='
    '0&include=ciso2&maxResults='
    '20&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Locations?'
    'adminDistrict=WA&locality=Seattle&o=xml&includeNeighborhood='
    '0&include=ciso2&maxResults='
    '20&key={0}'.format(BING_MAPS_KEY)
]


@parametrize('data,expected', [
    (DATA[0], EXPECTED[0]),
    (DATA[1], EXPECTED[1])
])
def test_schema_without_key(data, expected):
    schema = LocationByAddressQueryString()
    is_valid_schema = schema.validate(data)
    assert bool(is_valid_schema) is expected


@parametrize('data,expected', [
    (DATA[2], EXPECTED[2])
])
def test_consolidate_query_dict(data, expected):
    query = LocationByAddressQueryString()
    query_string = query.dump(data['queryParameters']).data
    assert query_string == expected


@parametrize('data,expected', [
    (DATA[3], EXPECTED[3])
])
def test_build_url_http_protocol(data, expected):
    loc_by_address = LocationByAddress(data, http_protocol)
    url = loc_by_address.build_url()
    assert url == expected


@parametrize('data,expected', [
    (DATA[4], EXPECTED[4]),
    (DATA[5], EXPECTED[5])
])
def test_build_url_https_protocol(data, expected):
    loc_by_address = LocationByAddress(data, https_protocol)
    url = loc_by_address.build_url()
    assert url == expected


@parametrize('data', [
    (DATA[0])
])
def test_schema_without_key_exception(data):
    with pytest.raises(KeyError) as exc:
        loc_by_address = LocationByAddress(data, https_protocol)
        schema = loc_by_address.build_url()
        assert exc == {'queryParameters': {'key': ['Please provide a key']}}


@parametrize('data', [
    ('')
])
def test_schema_no_data(data):
    with pytest.raises(TypeError) as exc:
        loc_by_address = LocationByAddress(data)
        assert exc == "No data given"
