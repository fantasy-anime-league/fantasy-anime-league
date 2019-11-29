import configparser
from unittest.mock import patch, MagicMock

import pytest
import vcr
import os

import fal.controllers.collect_series as collect_series
from fal.orm import Season, Anime

config = configparser.ConfigParser()
config.read("config.ini")

vcrpath = config["vcr"]["path"]


@pytest.mark.parametrize("season,year", [("spring", 2019)])
@vcr.use_cassette(f"{vcrpath}/collect_series/get-series.yaml")
def test_get_series(series_dict_fixture, season, year):
    series_dict = collect_series.get_series(year=int(year), season=season.lower())
    assert series_dict == series_dict_fixture


def test_output_series(series, shared_datadir):
    path = "test/unit/series_test.txt"
    collect_series.output_series(series, path)
    expected_series_list = (shared_datadir / "series_fixture.txt").read_text()
    with open(path) as test_f:
        assert test_f.read() == expected_series_list
    os.remove(path)


def test_output_series_titles(series_titles, shared_datadir):
    path = "test/unit/series_sorted_test.txt"
    collect_series.output_series_titles(series_titles, path)
    expected_sorted_series_list = (
        shared_datadir / "series_sorted_fixture.txt"
    ).read_text()
    with open(path) as test_f:
        assert test_f.read() == expected_sorted_series_list
    os.remove(path)
