from bingmaps import BING_MAPS_KEY
from bingmaps.location import LocationByAddress
from .fixtures import parametrie

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
             'key': BING_MAPS_KEY}},
        {'queryParameters':
            {'postalCode': 98052,
             'key': BING_MAPS_KEY
             }}
        ]


@parametrie('data', [
    (DATA[6])
])
def test_get_data_from_url(data):
    url = LocationByAddress(data)
    assert url.get_data().status_code == 200
