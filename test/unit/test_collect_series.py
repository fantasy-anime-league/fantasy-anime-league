from fixtures.collect_series_fixtures import *
from fal.models import Season, Anime
import fal.controllers.collect_series as collect_series

from unittest.mock import patch, MagicMock
import pytest
import vcr


@pytest.mark.parametrize("season,year", [
    ('spring', 2019),
])
@vcr.use_cassette('test/unit/fixtures/vcr_cassettes/collect_series/get-series.yaml')
def test_get_series(series_dict_fixture, season, year):
    series_dict = collect_series.get_series(
        year=int(year), season=season.lower())
    assert series_dict == series_dict_fixture


def test_output_series(series):
    path = 'test/unit/series_test.txt'
    collect_series.output_series(series, path)
    with open(path) as test_f, open('test/unit/fixtures/series_fixture.txt') as fixture_f:
        assert test_f.read() == fixture_f.read()


def test_output_series_titles(series_titles):
    path = 'test/unit/series_sorted_test.txt'
    collect_series.output_series_titles(series_titles, path)
    with open(path) as test_f, open('test/unit/fixtures/series_sorted_fixture.txt') as fixture_f:
        assert test_f.read() == fixture_f.read()
