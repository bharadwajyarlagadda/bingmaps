import pytest

parametrize = pytest.mark.parametrize
https_protocol = 'https'


@pytest.fixture
def create_tmp_dir(tmpdir):
    tmp_dir = tmpdir.mkdir('test_folder')
    return str(tmp_dir)
