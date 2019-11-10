from unittest.mock import MagicMock

from fal.orm import Season


def test_get_season_from_database_adds_season():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.one_or_none.return_value = None

    expected_season = Season(season_of_year="spring", year=2017)

    Season.get_season_from_database(
        expected_season.season_of_year, expected_season.year, mock_session
    )
    args, _ = mock_session.add.call_args
    season_added = args[0]
    assert isinstance(season_added, Season)
    assert season_added.year == expected_season.year
    assert season_added.season_of_year == expected_season.season_of_year
