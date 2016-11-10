import pytest
from personapi.api.run import app
from personapi.db.data_repository import DataFetcher


@pytest.fixture
def filepipepath():
    return "./testfiles/file-pipe.txt"


@pytest.fixture
def filecommapath():
    return "./testfiles/file-comma.txt"

@pytest.fixture
def filewhitespacepath():
    return "./testfiles/file-whitespace.txt"


@pytest.fixture()
def test_client():
    client = app.test_client()
    return client


@pytest.fixture()
def db_client():
    # Monkey patch the db_client so we can control it
    app.db_client = DataFetcher()
    return app.db_client
