from unittest.mock import patch

from fal.controllers import load_aces
from fal.models import TeamWeeklyAnime

def test_ace_already_loaded_this_week(team_weekly_anime_factory, team_factory, anime_factory, session):
    team = team_factory()
    anime = anime_factory.create_batch(3)
    team_weekly_anime_factory(team=team, anime=anime[0], week=2)
    team_weekly_anime_factory(team=team, anime=anime[1], week=2, ace=1)
    team_weekly_anime_factory(team=team, anime=anime[2], week=2)

    assert load_aces.ace_already_loaded_this_week(team, 2, session)


def test_ace_not_already_loaded_this_week(team_weekly_anime_factory, team_factory, anime_factory, session):
    team = team_factory()
    anime = anime_factory.create_batch(3)
    team_weekly_anime_factory(team=team, anime=anime[0], week=2)
    team_weekly_anime_factory(team=team, anime=anime[1], week=1, ace=1)
    team_weekly_anime_factory(team=team, anime=anime[2], week=2)

    assert not load_aces.ace_already_loaded_this_week(team, 2, session)

def test_team_anime_aced_already(team_weekly_anime_factory, team_factory, anime_factory, session):
    team = team_factory()
    anime = anime_factory()
    team_weekly_anime_factory(team=team, anime=anime, week=0)
    team_weekly_anime_factory(team=team, anime=anime, week=1, ace=1)
    team_weekly_anime_factory(team=team, anime=anime, week=2)

    assert load_aces.team_anime_aced_already(team, anime, session)

def test_team_anime_not_aced_already(team_weekly_anime_factory, team_factory, anime_factory, session):
    team = team_factory()
    anime = anime_factory()
    team_weekly_anime_factory(team=team, anime=anime, week=0)
    team_weekly_anime_factory(team=team, anime=anime, week=1)
    team_weekly_anime_factory(team=team, anime=anime, week=2)

    assert not load_aces.team_anime_aced_already(team, anime, session)

@patch('fal.controllers.load_aces.config')
@patch('fal.controllers.load_aces.session_scope')
def test_load_aces(
    # patches
    session_scope_mock,
    config_mock,
    #factories
    season_factory,
    team_factory,
    anime_factory,
    team_weekly_anime_factory,
    #fixtures
    config_functor,
    session_scope,
    session
):
    session_scope_mock.side_effect = session_scope

    config_function = config_functor(
        sections=[
            'season info',
            'weekly info'
        ],
        kv={
            'season': 'spring',
            'year': 2018,
            'current-week': 2
        }
    )
    config_mock.getint.side_effect = config_function
    config_mock.get.side_effect = config_function

    season = season_factory(season_of_year='spring', year=2018)
    teams = team_factory.create_batch(2, season=season)
    anime = anime_factory.create_batch(8, season=season)

    for week in range(3):
        for _anime in anime[:5]:
            team_weekly_anime_factory(
                team=teams[0],
                anime=_anime,
                week=week
            )

        for _anime in anime[-5:]:
            team_weekly_anime_factory(
                team=teams[1],
                anime=_anime,
                week=week
            )

    team0_previous_aced_anime = session.query(TeamWeeklyAnime).filter(
        TeamWeeklyAnime.week == 1,
        TeamWeeklyAnime.team == teams[0],
        TeamWeeklyAnime.anime == anime[0]
    ).one()
    team0_previous_aced_anime.ace = 1

    load_aces.load_aces([
        f"{teams[0].name} {anime[0].name}",
        f"{teams[1].name} {anime[7].name}",
    ])

    should_not_be_aced_again = session.query(TeamWeeklyAnime).filter(
        TeamWeeklyAnime.week == 2,
        TeamWeeklyAnime.team == teams[0],
        TeamWeeklyAnime.anime == anime[0]
    ).one()

    assert should_not_be_aced_again.ace == 0

    should_be_aced = session.query(TeamWeeklyAnime).filter(
        TeamWeeklyAnime.week == 2,
        TeamWeeklyAnime.team == teams[1],
        TeamWeeklyAnime.anime == anime[7]
    ).one()

    assert should_be_aced.ace == 1
