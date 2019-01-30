import pytest
import vcr

from src.check_usernames import check

@vcr.use_cassette('test/vcr_cassettes/check_usernames/check-username-success.yaml')
def test_check_username_success(capfd):
    check("Congress")
    out, _ = capfd.readouterr()
    assert out == "Congress\n"


@vcr.use_cassette('test/vcr_cassettes/check_usernames/check-username-failure.yaml')
def test_check_username_failure(capfd):
    check("Azertytreza2402")
    out, _ = capfd.readouterr()
    assert out == "Azertytreza2402\nusername doesn't exist anymore: Azertytreza2402\n"
