from unittest.mock import patch
import pytest

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import faker

from fal.models import Team, Season, SeasonOfYear, Anime, WeekSnapshotOfTeamAnime

fake = faker.Faker()
fake.add_provider(faker.providers.internet)


def test_create_and_retrieve_team_by_name(session):
    season = Season.get_or_create(SeasonOfYear.SPRING, 2006, session)
    username = fake.user_name()
    team = Team.create(username, season, session)

    assert team == Team.get_by_name(username, season, session)


def test_retrieve_team_does_not_exist(session):
    season2006 = Season.get_or_create(SeasonOfYear.SPRING, 2006, session)
    season2007 = Season.get_or_create(SeasonOfYear.SPRING, 2007, session)
    username = fake.user_name()
    team = Team.create(username, season2006, session)

    with pytest.raises(NoResultFound):
        Team.get_by_name(username, season2007, session)


def test_create_team_twice_throws_exception(session):
    season = Season.get_or_create(SeasonOfYear.SPRING, 2006, session)
    username = fake.user_name()
    Team.create(username, season, session)
    with pytest.raises(AssertionError):
        Team.create(username, season, session)


@patch("fal.models.team.config")
def test_add_same_anime_to_team_raises_exception(
    # patches
    config_mock,
    # fixtures
    session,
    config_functor,
):
    config_function = config_functor(sections=["weekly info"], kv={"current-week": 0})
    config_mock.getint.side_effect = config_function

    season = Season.get_or_create(SeasonOfYear.SPRING, 2006, session)
    anime = Anime.create(1234, "The Melancholy of Haruhi Suzumiya", season, session)
    team = Team.create(fake.user_name(), season, session)
    team.add_anime_to_team(anime)
    with pytest.raises(IntegrityError):
        team.add_anime_to_team(anime, True)


@patch("fal.models.season.config")
@patch("fal.models.team.config")
def test_bench_swap(
    # patches
    team_config_mock,
    season_config_mock,
    # fixtures
    session,
    config_functor,
):
    config_function = config_functor(
        sections=["weekly info", "season info"],
        kv={"current-week": 0, "min-weeks-between-bench-swaps": 3},
    )
    team_config_mock.getint.side_effect = config_function

    config_function = config_functor(
        sections=["weekly info"],
        kv={"current-week": 0},
    )
    season_config_mock.getint.side_effect = config_function

    season = Season.get_or_create(SeasonOfYear.SPRING, 2006, session)
    haruhi = Anime.create(1234, "The Melancholy of Haruhi Suzumiya", season, session)
    bebop = Anime.create(4321, "Cowboy Bebop", season, session)
    team = Team.create("kei-clone", season, session)
    team.add_anime_to_team(haruhi)
    team.add_anime_to_team(bebop, True)

    with pytest.raises(AssertionError):
        # this should fail since bench and active are swapped
        team.bench_swap(active_anime=bebop, bench_anime=haruhi, week=0)

    team.bench_swap(active_anime=haruhi, bench_anime=bebop, week=0)

    week_snapshot = team.get_anime(week=0)
    assert week_snapshot == WeekSnapshotOfTeamAnime(
        week=0, active=[bebop], bench=[haruhi]
    )

    with pytest.raises(AssertionError):
        # this should fail since we just swapped this week
        team.bench_swap(active_anime=bebop, bench_anime=haruhi, week=0)

    for week in range(1, 5):
        season.current_week = week
        season.init_new_week()

    config_function = config_functor(
        sections=["weekly info", "season info"],
        kv={"current-week": 4, "min-weeks-between-bench-swaps": 3},
    )
    season_config_mock.getint.side_effect = config_function

    team.bench_swap(active_anime=bebop, bench_anime=haruhi, week=4)
    week_snapshot = team.get_anime(week=4)
    assert week_snapshot == WeekSnapshotOfTeamAnime(
        week=4, active=[haruhi], bench=[bebop]
    )
