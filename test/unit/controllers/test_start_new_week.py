from unittest.mock import patch

from fal.controllers.start_new_week import StartNewWeek
from fal.models import Season
from fal.orm import TeamWeeklyAnime


def test_init_new_team_weekly_anime(
    # factories
    orm_season_factory,
    orm_team_factory,
    team_weekly_anime_factory,
    # fixtures
    session,
):
    season = orm_season_factory()
    teams = orm_team_factory.create_batch(10, season=season)
    for team in teams:
        for week in range(1, 4, 1):
            team_weekly_anime_factory.create_batch(5, team=team, week=week)

    start_new_week = StartNewWeek(current_week=4)
    start_new_week._execute(
        session=session, season=Season.from_orm_season(season, session)
    )

    for team in teams:
        anime_in_week_4 = (
            session.query(TeamWeeklyAnime)
            .filter(TeamWeeklyAnime.week == 4, TeamWeeklyAnime.team_id == team.id)
            .all()
        )
        assert len(anime_in_week_4) == 5
