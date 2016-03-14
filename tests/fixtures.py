import pytest

parametrize = pytest.mark.parametrize
https_protocol = 'https'

BING_MAPS_KEY = 'Av6_H8GIYQyP-DLQwLOKDknW64Qfm' \
                'VgJmVpfiSO861v0x_j1pLPCOW6s-70nCzEW'


@pytest.fixture
def create_tmp_dir(tmpdir):
    tmp_dir = tmpdir.mkdir('test_folder')
    return str(tmp_dir)
