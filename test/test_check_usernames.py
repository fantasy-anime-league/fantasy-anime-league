import pytest
import vcr

from src.check_usernames import check

@vcr.use_cassette('test/vcr_cassettes/check-success.yaml')
def test_check_success(capfd):
    check("Congress")
    out, err = capfd.readouterr()
    assert out == "Congress\n"


@vcr.use_cassette('test/vcr_cassettes/check-failure.yaml')
def test_check_failure(capfd):
    check("Azertytreza2402")
    out, err = capfd.readouterr()
    assert out == "Azertytreza2402\nusername doesn't exist anymore: Azertytreza2402\n"
