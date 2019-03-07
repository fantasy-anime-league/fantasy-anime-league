from fixtures.ptw_counter_fixtures import *
import fal.ptw_counter as ptw_counter

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
