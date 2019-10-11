import configparser

import pytest
import vcr

from fal.controllers.check_usernames import check

config = configparser.ConfigParser()
config.read("config.ini")

vcrpath = config["vcr"]["path"]


@vcr.use_cassette(f"{vcrpath}/check_usernames/check-username-success.yaml")
def test_check_username_success(capfd):
    check("Congress")
    out, _ = capfd.readouterr()
    assert out == "Congress\n"


@vcr.use_cassette(f"{vcrpath}/check_usernames/check-username-failure.yaml")
def test_check_username_failure(capfd):
    check("Azertytreza2402")
    out, _ = capfd.readouterr()
    assert out == "Azertytreza2402\nusername doesn't exist anymore: Azertytreza2402\n"


@vcr.use_cassette(f"{vcrpath}/check_usernames/caps-username-success.yaml")
def test_caps_username_success(capfd):
    check("alExThEriOt")
    out, _ = capfd.readouterr()
    assert out == "alExThEriOt\n"
