import pytest

parametrie = pytest.mark.parametrize


@pytest.fixture
def create_tmp_dir(tmpdir):
    tmp_dir = tmpdir.mkdir('test_folder')
    return str(tmp_dir)
