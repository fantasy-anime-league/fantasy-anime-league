from unittest.mock import patch

from fal.controllers import start_new_week
from fal.orm import TeamWeeklyAnime, Season
from fal.models import Season, SeasonOfYear


@patch("fal.controllers.start_new_week.config")
@patch("fal.controllers.start_new_week.session_scope")
def test_init_new_team_weekly_anime(
    # patches
    session_scope_mock,
    start_new_week_config_mock,
    # factories
    season_factory,
    orm_team_factory,
    team_weekly_anime_factory,
    # fixtures
    config_functor,
    session_scope,
    session,
):
    season = season_factory(session=session)

    session_scope_mock.side_effect = session_scope

    config_function = config_functor(
        sections=["season info"],
        kv={"season": season.season_of_year.value, "year": season.year},
    )
    start_new_week_config_mock.getint.side_effect = config_function
    start_new_week_config_mock.get.side_effect = config_function

    season.current_week = 4

    teams = orm_team_factory.create_batch(10, season=season._entity)
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
