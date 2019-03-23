from unittest.mock import patch
import pytest

from fal.views import teams
from fal.models import TeamWeeklyAnime, Team, Anime

import os


@patch('fal.views.teams.session_scope')
def test_headcount(session_scope_mock, session, session_scope, season_factory, shared_datadir):
    session_scope_mock.side_effect = session_scope

    team_list = [
        Team(name='kei-clone'),
        Team(name='abhinavk99'),
        Team(name='Congress')
    ]
    season = season_factory(id=0, teams=team_list)

    path = 'team_headcount.txt'
    teams.headcount(season.season_of_year, season.year, path)
    exp_headcount = (shared_datadir / 'exp_team_headcount.txt').read_text()
    with open(path) as test_f:
        # Ignore first line with season and year info
        assert test_f.read().split('\n')[1:] == exp_headcount.split('\n')[1:]
    os.remove(path)


@patch('fal.views.teams.config')
@patch('fal.views.teams.session_scope')
def test_team_overview(session_scope_mock, config_mock, session, session_scope, season_factory,
                       shared_datadir, team_factory, team_weekly_anime_factory, anime_factory):
    def mock_config_getweek(section, key):
        assert section == "weekly info"
        assert key == "current-week"
        return 0

    config_mock.getint.side_effect = mock_config_getweek

    session_scope_mock.side_effect = session_scope

    season = season_factory(id=0)
    anime = [
        anime_factory(name='Jojo no Kimyou na Bouken: Ougon no Kaze'),
        anime_factory(name='Radiant'),
        anime_factory(name='Gakuen Basara'),
        anime_factory(name='Bakumatsu'),
    ]
    team_list = [
        team_factory(name='kei-clone'),
        team_factory(name='abhinavk99')
    ]
    team_weekly_anime_list = [
        team_weekly_anime_factory(team_id=team_list[0].id, anime=anime[2]),
        team_weekly_anime_factory(
            team_id=team_list[0].id, anime=anime[3], bench=True),
        team_weekly_anime_factory(team_id=team_list[1].id, anime=anime[0]),
        team_weekly_anime_factory(
            team_id=team_list[1].id, anime=anime[1], bench=True),
    ]

    path = 'team_overview.txt'
    teams.team_overview(season.season_of_year, season.year, path)
    exp_overview = (shared_datadir / 'exp_team_overview.txt').read_text()
    with open(path) as test_f:
        # Ignore first line with season and year info
        assert test_f.read().split('\n')[1:] == exp_overview.split('\n')[1:]
    os.remove(path)


@patch('fal.views.teams.config')
@patch('fal.views.teams.session_scope')
def test_team_stats(session_scope_mock, config_mock, session, session_scope, season_factory,
                    shared_datadir, team_factory, team_weekly_anime_factory, anime_factory):
    def mock_config_getweek(section, key):
        assert section == "weekly info"
        assert key == "current-week"
        return 0

    config_mock.getint.side_effect = mock_config_getweek

    session_scope_mock.side_effect = session_scope

    season = season_factory(id=0)
    anime = [
        anime_factory(name='Jojo no Kimyou na Bouken: Ougon no Kaze'),
        anime_factory(name='Kaze ga Tsuyoku Fuiteiru'),
        anime_factory(
            name='Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo'),
    ]
    team_list = [
        team_factory(name='kei-clone'),
        team_factory(name='abhinavk99')
    ]
    team_weekly_anime_list = [
        team_weekly_anime_factory(team_id=team_list[0].id, anime=anime[2]),
        team_weekly_anime_factory(
            team_id=team_list[0].id, anime=anime[0], bench=True),
        team_weekly_anime_factory(team_id=team_list[1].id, anime=anime[0]),
        team_weekly_anime_factory(
            team_id=team_list[1].id, anime=anime[1], bench=True),
    ]

    path = 'team_stats.txt'
    teams.team_stats(season.season_of_year, season.year, path)
    exp_team_stats = (shared_datadir / 'exp_team_stats.txt').read_text()
    with open(path) as test_f:
        assert test_f.read() == exp_team_stats
    os.remove(path)


@patch('fal.views.teams.config')
@patch('fal.views.teams.session_scope')
def test_team_dist(session_scope_mock, config_mock, session, session_scope, season_factory,
                   shared_datadir, team_factory, team_weekly_anime_factory, anime_factory):
    def mock_config_getweek(section, key):
        assert section == "weekly info"
        assert key == "current-week"
        return 0

    config_mock.getint.side_effect = mock_config_getweek

    session_scope_mock.side_effect = session_scope

    season = season_factory(id=0)
    anime = [
        anime_factory(name='Jojo no Kimyou na Bouken: Ougon no Kaze'),
        anime_factory(name='Kaze ga Tsuyoku Fuiteiru'),
        anime_factory(
            name='Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo'),
    ]
    team_list = [
        team_factory(name='kei-clone'),
        team_factory(name='abhinavk99'),
        team_factory(name='Congress')
    ]
    team_weekly_anime_list = [
        team_weekly_anime_factory(
            team_id=team_list[0].id, anime=anime[0], bench=True),
        team_weekly_anime_factory(team_id=team_list[0].id, anime=anime[1]),
        team_weekly_anime_factory(team_id=team_list[1].id, anime=anime[0]),
        team_weekly_anime_factory(
            team_id=team_list[1].id, anime=anime[1], bench=True),
        team_weekly_anime_factory(team_id=team_list[2].id, anime=anime[0]),
        team_weekly_anime_factory(
            team_id=team_list[2].id, anime=anime[2], bench=True),
    ]

    path = 'team_dist.txt'
    teams.team_dist(season.season_of_year, season.year, path)
    exp_team_dist = (shared_datadir / 'exp_team_dist.txt').read_text()
    with open(path) as test_f:
        assert test_f.read() == exp_team_dist
    os.remove(path)


def test_write_teams_to_file(shared_datadir):
    team_list = [
        [Team(name='kei-clone'), Team(name='abhinavk99')],
        [Team(name='Congress'), Team(name='Naruleach')]
    ]

    path = 'same_teams.txt'
    with open(path, 'w') as f:
        teams.write_teams_to_file(f, 0, team_list, teams.SAME_SPLIT_TEXT)
    exp_same_teams = (shared_datadir / 'exp_same_teams.txt').read_text()
    with open(path) as test_f:
        assert test_f.read() == exp_same_teams
    os.remove(path)


def test_get_dist():
    anime = (
        TeamWeeklyAnime(anime_id=1),
        TeamWeeklyAnime(anime_id=2),
        TeamWeeklyAnime(anime_id=3),
    )
    team_list = (
        Team(name='kei-clone'),
        Team(name='abhinavk99'),
        Team(name='Congress'),
        Team(name='Naruleach'),
        Team(name='AlexTheRiot')
    )
    team_dict = {
        (anime[0], anime[1]): [team_list[0], team_list[1]],
        (anime[0], anime[2]): [team_list[2], team_list[3]],
        (anime[1], anime[2]): [team_list[4]]
    }
    num_unique, same_teams = teams.get_dist(team_dict)
    assert num_unique == 1
    assert same_teams == [
        [team_list[0], team_list[1]],
        [team_list[2], team_list[3]]
    ]
