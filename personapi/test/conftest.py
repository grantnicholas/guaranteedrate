import pytest


@pytest.fixture
def filepipepath():
    return "/home/grant/PycharmProjects/GuaranteedRate/personapi/test/testfiles/file-pipe.txt"


@pytest.fixture
def filecommapath():
    return "/home/grant/PycharmProjects/GuaranteedRate/personapi/test/testfiles/file-comma.txt"

@pytest.fixture
def filewhitespacepath():
    return "/home/grant/PycharmProjects/GuaranteedRate/personapi/test/testfiles/file-whitespace.txt"