import configparser
import os
from datetime import date
from unittest.mock import patch, MagicMock


import pytest
import vcr

from fal.models import PlanToWatch, Anime
import fal.controllers.ptw_counter as ptw_counter


config = configparser.ConfigParser()
config.read("config.ini")

vcrpath = config["vcr"]["path"]


def test_localize_number():
    assert ptw_counter.localize_number(1034) == "1,034"


@patch("fal.controllers.ptw_counter.time")
@pytest.mark.parametrize(
    "anime_list",
    [
        (
            [
                Anime(id=34134, name="One Punch Man Season 2", season_id=2),
                Anime(id=38524, name="Shingeki no Kyojin Season 3 Part 2", season_id=2),
            ]
        )
    ],
)
@vcr.use_cassette(f"{vcrpath}/ptw_counter/get-ptw-info.yaml")
def test_get_ptw_info(time_mock, ptw_fixture, anime_list):
    time_mock.sleep.return_value = None  # no need to wait in a unit test!
    ptw = ptw_counter.get_ptw_info(anime_list)
    assert ptw == ptw_fixture


@pytest.mark.parametrize(
    "season_of_year, year, ptw",
    [
        (
            "spring",
            2019,
            [
                ptw_counter.PTWEntry("One Punch Man Season 2", 34134, "311,499"),
                ptw_counter.PTWEntry(
                    "Shingeki no Kyojin Season 3 Part 2", 38524, "98,614"
                ),
            ],
        )
    ],
)
def test_output_ptw_info(season_of_year, year, ptw, shared_datadir):
    path = f"{season_of_year.capitalize()}-{str(year)}-{str(date.today())}.csv"
    ptw_counter.output_ptw_info(season_of_year, year, ptw)
    expected_ptw = (shared_datadir / "ptw_info_fixture.csv").read_text()
    with open(path) as test_f:
        assert test_f.read() == expected_ptw
    os.remove(path)


def test_add_ptw_to_database():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.one_or_none.return_value = None

    expected_ptw_entry = PlanToWatch(anime_id=34134, date=date.today(), count=311499)

    ptw_counter.add_ptw_to_database(
        expected_ptw_entry.anime_id,
        expected_ptw_entry.date,
        expected_ptw_entry.count,
        mock_session,
    )

    args, _ = mock_session.add.call_args
    ptw_entry_added = args[0]
    assert isinstance(ptw_entry_added, PlanToWatch)
    assert ptw_entry_added.anime_id == expected_ptw_entry.anime_id
    assert ptw_entry_added.date == expected_ptw_entry.date
    assert ptw_entry_added.count == expected_ptw_entry.count


def test_update_ptw_in_database():
    mock_session = MagicMock()

    expected_ptw_entry = PlanToWatch(anime_id=34134, date=date.today(), count=311499)
    mock_session.query.return_value.filter.return_value.one_or_none.return_value = (
        expected_ptw_entry
    )

    ptw_counter.add_ptw_to_database(
        expected_ptw_entry.anime_id, expected_ptw_entry.date, 1, mock_session
    )

    mock_session.commit.assert_called_once()
