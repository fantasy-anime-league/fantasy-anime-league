from unittest.mock import patch

from fal.controllers import init_new_week
from fal.orm import TeamWeeklyAnime, Season


@patch("fal.controllers.init_new_week.config")
@patch("fal.controllers.init_new_week.session_scope")
def test_init_new_team_weekly_anime(
    # patches
    session_scope_mock,
    config_mock,
    # factories
    season_factory,
    team_factory,
    team_weekly_anime_factory,
    # fixtures
    config_functor,
    session_scope,
    session,
):
    session_scope_mock.side_effect = session_scope

    config_function = config_functor(
        sections=["season info", "weekly info"],
        kv={"season": "spring", "year": 2018, "current-week": 4},
    )
    config_mock.getint.side_effect = config_function
    config_mock.get.side_effect = config_function

    season = season_factory(season_of_year="spring", year=2018)
    teams = team_factory.create_batch(10, season=season)
    for team in teams:
        for week in range(1, 4, 1):
            team_weekly_anime_factory.create_batch(5, team=team, week=week)

    init_new_week.init_new_team_weekly_anime()

    for team in teams:
        anime_in_week_4 = (
            session.query(TeamWeeklyAnime)
            .filter(TeamWeeklyAnime.week == 4, TeamWeeklyAnime.team_id == team.id)
            .all()
        )
        assert len(anime_in_week_4) == 5
