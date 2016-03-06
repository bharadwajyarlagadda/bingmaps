from bingmaps.utils.url_structure import QueryParameters, build_url
from bingmaps.location import LocationByAddress
from .fixtures import parametrie
from bingmaps import BING_MAPS_KEY
import pytest

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
    '1&include=ciso2&maxResults=20&key=abs',
    'http://dev.virtualearth.net/REST/v1/Locations?'
    'adminDistrict=WA&locality=Seattle&includeNeighborhood='
    '1&include=ciso2&maxResults='
    '20&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Locations?'
    'adminDistrict=WA&locality=Seattle&includeNeighborhood='
    '1&include=ciso2&maxResults='
    '20&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Locations?'
    'adminDistrict=WA&locality=Seattle&o=xml&includeNeighborhood='
    '1&include=ciso2&maxResults='
    '20&key={0}'.format(BING_MAPS_KEY)
]


@parametrie('data,expected',
            [
                (DATA[0], EXPECTED[0])
            ])
def test_schema_without_key(data, expected):
    schema = QueryParameters()
    is_valid_schema = schema.validate(data)
    assert bool(is_valid_schema) is expected


@parametrie('data,expected',
            [
                (DATA[1], EXPECTED[1])
            ])
def test_schema_with_key(data, expected):
    schema = QueryParameters()
    is_valid_schema = schema.validate(data)
    assert bool(is_valid_schema) is expected


@parametrie('data,expected',
            [
                (DATA[2], EXPECTED[2])
            ])
def test_consolidate_query_dict(data, expected):
    query = QueryParameters()
    query_string = query.dump(data['queryParameters']).data
    assert query_string == expected


@parametrie('data,expected',
            [
                (DATA[3], EXPECTED[3])
            ])
def test_build_url_http_protocol(data, expected):
    loc_by_address = LocationByAddress(data)
    url = loc_by_address.build_url(data, http_protocol)
    assert url == expected


@parametrie('data,expected',
            [
                (DATA[4], EXPECTED[4])
            ])
def test_build_url_https_protocol(data, expected):
    loc_by_address = LocationByAddress(data)
    url = loc_by_address.build_url(data, https_protocol)
    assert url == expected


@parametrie('data,expected',
            [
                (DATA[5], EXPECTED[5])
            ])
def test_build_url_https_protocol_output_xml(data, expected):
    loc_by_address = LocationByAddress(data)
    url = loc_by_address.build_url(data, https_protocol)
    assert url == expected


@parametrie('data',
            [
                (DATA[0])
            ])
def test_schema_without_key1(data):
    loc_by_address = LocationByAddress(data)
    with pytest.raises(KeyError) as exc:
        schema = loc_by_address.build_url(data, https_protocol)
