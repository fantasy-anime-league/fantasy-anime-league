from fixtures.ptw_counter_fixtures import *
from fal.models import PlanToWatch
import fal.ptw_counter as ptw_counter

from unittest.mock import patch, MagicMock

import pytest
import vcr
from datetime import date


def test_localize_number():
    assert ptw_counter.localize_number(1034) == '1,034'


@pytest.mark.parametrize("series_dict", [
    ({34134: 'One Punch Man Season 2', 38524: 'Shingeki no Kyojin Season 3 Part 2'}),
])
@vcr.use_cassette('test/unit/fixtures/vcr_cassettes/ptw_counter/get-ptw-info.yaml')
def test_get_ptw_info(ptw_fixture, series_dict):
    ptw = ptw_counter.get_ptw_info(series_dict)
    assert ptw == ptw_fixture


@pytest.mark.parametrize("season_of_year, year, ptw", [
    ('spring', 2019, [('One Punch Man Season 2', 34134, '311,499'),
                      ('Shingeki no Kyojin Season 3 Part 2', 38524, '98,614')]),
])
def test_output_ptw_info(season_of_year, year, ptw):
    directory = 'test/unit'
    path = directory + \
        f'/{season_of_year.capitalize()}-{str(year)}-{str(date.today())}.csv'
    ptw_counter.output_ptw_info(season_of_year, year, ptw, directory)
    with open(path) as test_f, open('test/unit/fixtures/ptw_info_fixture.csv') as fixture_f:
        assert test_f.read() == fixture_f.read()


def test_add_ptw_to_database():
    mock_session = MagicMock()

    expected_ptw_entry = PlanToWatch(
        anime_id=34134, date=date.today(), count=311499)

    ptw_counter.add_ptw_to_database(
        expected_ptw_entry.anime_id, expected_ptw_entry.date, expected_ptw_entry.count, mock_session)

    args, _ = mock_session.add.call_args
    ptw_entry_added = args[0]
    assert isinstance(ptw_entry_added, PlanToWatch)
    assert ptw_entry_added.anime_id == expected_ptw_entry.anime_id
    assert ptw_entry_added.date == expected_ptw_entry.date
    assert ptw_entry_added.count == expected_ptw_entry.count
