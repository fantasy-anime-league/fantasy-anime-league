from unittest.mock import patch

from fal.controllers import start_new_week
from fal.orm import TeamWeeklyAnime, Season
from fal.models import Season, SeasonOfYear


@patch("fal.models.season.config")
@patch("fal.controllers.start_new_week.config")
@patch("fal.controllers.start_new_week.session_scope")
def test_init_new_team_weekly_anime(
    # patches
    session_scope_mock,
    start_new_week_config_mock,
    season_config_mock,
    # factories
    team_factory,
    team_weekly_anime_factory,
    # fixtures
    config_functor,
    session_scope,
    session,
):
    session_scope_mock.side_effect = session_scope

    config_function = config_functor(
        sections=["season info"], kv={"season": "spring", "year": 2018},
    )
    start_new_week_config_mock.getint.side_effect = config_function
    start_new_week_config_mock.get.side_effect = config_function

    config_function = config_functor(sections=["weekly info"], kv={"current-week": 4},)
    season_config_mock.getint.side_effect = config_function

    season = Season.get_or_create(
        season_of_year=SeasonOfYear.SPRING, year=2018, session=session
    )
    teams = team_factory.create_batch(10, season=season._entity)
    for team in teams:
        for week in range(1, 4, 1):
            team_weekly_anime_factory.create_batch(5, team=team, week=week)

    start_new_week.start_new_week()

    for team in teams:
        anime_in_week_4 = (
            session.query(TeamWeeklyAnime)
            .filter(TeamWeeklyAnime.week == 4, TeamWeeklyAnime.team_id == team.id)
            .all()
        )
        assert len(anime_in_week_4) == 5
