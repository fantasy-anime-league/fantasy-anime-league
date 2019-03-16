from fixtures.collect_series_fixtures import series_dict_fixture, series, series_titles
from fal.models import Season, Anime
import fal.collect_series as collect_series

from unittest.mock import patch, MagicMock
import pytest
import vcr
import os


@pytest.mark.parametrize("season,year", [
    ('spring', 2019),
])
@vcr.use_cassette('test/unit/fixtures/vcr_cassettes/collect_series/get-series.yaml')
def test_get_series(series_dict_fixture, season, year):
    series_dict = collect_series.get_series(
        year=int(year), season=season.lower())
    assert series_dict == series_dict_fixture


def test_output_series(series, shared_datadir):
    path = 'test/unit/series_test.txt'
    collect_series.output_series(series, path)
    expected_series_list = (shared_datadir / 'series_fixture.txt').read_text()
    with open(path) as test_f:
        assert test_f.read() == expected_series_list
    os.remove(path)


def test_output_series_titles(series_titles, shared_datadir):
    path = 'test/unit/series_sorted_test.txt'
    collect_series.output_series_titles(series_titles, path)
    expected_sorted_series_list = (
        shared_datadir / 'series_sorted_fixture.txt').read_text()
    with open(path) as test_f:
        assert test_f.read() == expected_sorted_series_list
    os.remove(path)


def test_get_season_from_database_adds_season():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.one_or_none.return_value = None

    expected_season = Season(season_of_year="spring", year=2017)

    collect_series.get_season_from_database(
        expected_season.season_of_year, expected_season.year, mock_session)
    args, _ = mock_session.add.call_args
    season_added = args[0]
    assert isinstance(season_added, Season)
    assert season_added.year == expected_season.year
    assert season_added.season_of_year == expected_season.season_of_year


def test_add_anime_to_database():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.one_or_none.return_value = None

    expected_anime = Anime(id=1234,
                           name="The Melancholy of Haruhi Suzumiya", season_id=0)

    collect_series.add_anime_to_database(
        expected_anime.id, expected_anime.name, Season(id=expected_anime.season_id), mock_session)
    args, _ = mock_session.add.call_args
    anime_added = args[0]
    assert isinstance(anime_added, Anime)
    assert anime_added.id == expected_anime.id
    assert anime_added.name == expected_anime.name
    assert anime_added.season_id == expected_anime.season_id
