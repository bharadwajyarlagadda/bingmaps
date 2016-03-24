from bingmaps.apiservices import LocationByQuery
from .fixtures import parametrize, https_protocol, BING_MAPS_KEY

DATA = [
    {
        'q': '8672 Eagle Road Teaneck, NJ 07666',
        'key': BING_MAPS_KEY
    },
    {
        'q': '7266 Canterbury Court Oshkosh, WI 54901',
        'key': BING_MAPS_KEY
    },
    {
        'q': '9159 Highland Avenue Danbury, CT 06810',
        'key': BING_MAPS_KEY
    },
    {
        'q': '9106 Lakeview Drive Madison Heights, MI 48071',
        'key': BING_MAPS_KEY
    },
    {
        'q': '4566 Clay Street Bolingbrook, IL 60440',
        'key': BING_MAPS_KEY
    },
    {
        'q': '4856 Lawrence Street Burke, VA 22015',
        'key': BING_MAPS_KEY
    },
]

EXPECTED = [
    'http://dev.virtualearth.net/REST/v1/Locations?q='
    '8672%20Eagle%20Road%20Teaneck%2C%20NJ%2007666&includeNeighborhood='
    '0&include=ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
    'http://dev.virtualearth.net/REST/v1/Locations?q='
    '7266%20Canterbury%20Court%20Oshkosh%2C%20WI%2054901&includeNeighborhood='
    '0&include=ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
    'http://dev.virtualearth.net/REST/v1/Locations?q='
    '9159%20Highland%20Avenue%20Danbury%2C%20CT%2006810&includeNeighborhood='
    '0&include=ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Locations?q='
    '9106%20Lakeview%20Drive%20Madison%20Heights%2C%20MI%2048071&'
    'includeNeighborhood=0&include=ciso2&maxResults=20&key='
    '{0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Locations?q='
    '4566%20Clay%20Street%20Bolingbrook%2C%20IL%2060440&includeNeighborhood='
    '0&include=ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY),
    'https://dev.virtualearth.net/REST/v1/Locations?q='
    '4856%20Lawrence%20Street%20Burke%2C%20VA%2022015&includeNeighborhood='
    '0&include=ciso2&maxResults=20&key={0}'.format(BING_MAPS_KEY)
]


@parametrize('data,expected', [
    (DATA[0], EXPECTED[0]),
    (DATA[1], EXPECTED[1]),
    (DATA[2], EXPECTED[2])
])
def test_location_by_query_url_http_protocol(data, expected):
    loc_by_query = LocationByQuery(data)
    assert loc_by_query.build_url() == expected


@parametrize('data,expected', [
    (DATA[3], EXPECTED[3]),
    (DATA[4], EXPECTED[4]),
    (DATA[5], EXPECTED[5])
])
def test_location_by_query_url_https_protocol(data, expected):
    loc_by_query = LocationByQuery(data, https_protocol)
    assert loc_by_query.build_url() == expected
