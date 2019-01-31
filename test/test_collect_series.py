import pytest
import vcr
import json

from src.collect_series import get_series, output_series, output_series_titles
from fixtures.collect_series_fixtures import *


@vcr.use_cassette('test/fixtures/vcr_cassettes/collect_series/get-series.yaml')
def test_get_series(series_dict_fixture):
    with open('test/fixtures/series_info.json') as season_json:
        season_info = json.load(season_json)
        series_dict = get_series(season_info)
        assert series_dict == series_dict_fixture


@vcr.use_cassette('test/fixtures/vcr_cassettes/collect_series/output-series.yaml')
def test_output_series(capfd, series):
    path = 'test/series_test.txt'
    output_series(series, path)
    with open(path) as test_f, open('test/fixtures/series_fixture.txt') as fixture_f:
        assert test_f.read() == fixture_f.read()


@vcr.use_cassette('test/fixtures/vcr_cassettes/collect_series/output-series-titles.yaml')
def test_output_series_titles(capfd, series_titles):
    path = 'test/series_sorted_test.txt'
    output_series_titles(series_titles, path)
    with open(path) as test_f, open('test/fixtures/series_sorted_fixture.txt') as fixture_f:
        assert test_f.read() == fixture_f.read()
