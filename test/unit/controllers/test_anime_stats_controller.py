from unittest.mock import patch
import configparser
import pytest
import vcr
import factory

from fal.controllers.anime_stats import AnimeStats
import fal.models
from fal.orm import AnimeWeeklyStat, Anime, Season

config = configparser.ConfigParser()
config.read("config.ini")


vcrpath = config.get("vcr", "path")

DROPPED_POINTS = -4
SIMULCAST_POINTS = 2000
LICENSE_POINTS = 10000


def total_points_with_dropped(stats, num_regions, is_licensed, multiplier):
    return (
        multiplier * (stats.watching + stats.completed)
        + DROPPED_POINTS * stats.dropped
    )


def total_points_with_simulcast(stats, num_regions, is_licensed, multiplier):
    return (
        multiplier * (stats.watching + stats.completed)
        + SIMULCAST_POINTS * num_regions
    )


def total_points_with_license(stats, num_regions, is_licensed, multiplier):
    return multiplier * (stats.watching + stats.completed) + (
        LICENSE_POINTS if is_licensed else 0
    )

@patch("fal.controllers.anime_stats.AnimeStats._extract_file_contents")
@patch("fal.controllers.anime_stats.AnimeStats.get_forum_posts")
@patch("fal.controllers.anime_stats.config")
@patch("fal.models.season.config")
@pytest.mark.parametrize(
    "week,points,total_points_function,section",
    [
        ("4", DROPPED_POINTS, total_points_with_dropped, "scoring.dropped"),
        ("5", SIMULCAST_POINTS, total_points_with_simulcast, "scoring.simulcast"),
        ("13", LICENSE_POINTS, total_points_with_license, "scoring.license"),
    ],
)
@vcr.use_cassette(f"{vcrpath}/anime_stats/populate_anime_weekly_stats.yaml")
def test_populate_anime_weekly_stats(
    # mocks
    season_config_mock,
    anime_stats_config_mock,
    get_forum_posts,
    extract_file_contents,
    # factories
    config_functor,
    orm_season_factory,
    orm_anime_factory,
    orm_team_factory,
    team_weekly_anime_factory,
    anime_stats_factory,
    session,
    session_scope,
    # params
    week,
    points,
    total_points_function,
    section,
):
    config_function = config_functor(
        sections=["season info", section],
        kv={
            week: points,
            "min-weeks-between-bench-swaps": 3
        },
    )
    anime_stats_config_mock.getint.side_effect = config_function
    anime_stats_config_mock.get.side_effect = config_function
    season_config_mock.getint.side_effect = config_function

    extract_file_contents = lambda: None

    get_forum_posts.return_value = 0

    orm_season = orm_season_factory(id=1, season_of_year="spring", year=2018)
    cowboy_bebop = orm_anime_factory(id=1, name="Cowboy Bebop", season=orm_season)
    haruhi = orm_anime_factory(id=849, name="Suzumiya Haruhi no Yuuutsu", season=orm_season)
    opm = orm_anime_factory(id=30276, name="One Punch Man", season=orm_season)

    # Only 1 out of 34 teams owns Haruhi, which is <= 3%
    teams = orm_team_factory.create_batch(34, season=orm_season)
    team_weekly_anime_factory(team=teams[0], anime=cowboy_bebop, week=week)
    team_weekly_anime_factory(team=teams[0], anime=haruhi, week=week)
    for team in teams[1:]:
        team_weekly_anime_factory(team=team, anime=cowboy_bebop, week=week)
        team_weekly_anime_factory(team=team, anime=opm, week=week)

    anime_simulcast_region_counts = {1: 4, 849: 2, 30276: 3}
    licensed_anime = {849, 30276}

    anime_stats = anime_stats_factory(current_week=int(week))
    anime_stats.forum_post_week_interval = 2
    anime_stats.forum_post_multiplier = 25
    anime_stats.percent_ownership_for_double_score = 3
    anime_stats.licenses_lines = ["Suzumiya Haruhi no Yuuutsu", "One Punch Man"]
    anime_stats.simulcast_lines = [
        "Cowboy Bebop = simul simul simul simul",
        "Suzumiya Haruhi no Yuuutsu = simul randomstring simul",
        "One Punch Man = simul simul randomstring simul",
    ]

    season = fal.models.Season.from_orm_season(orm_season, session)
    anime_stats._execute(session, season)

    stats = session.query(AnimeWeeklyStat).order_by(AnimeWeeklyStat.anime_id).all()

    assert len(stats) == 3

    assert stats[0].watching == 71944
    assert stats[0].completed == 526969
    assert stats[0].anime_id == 1
    assert stats[0].total_points == total_points_function(
        stats=stats[0],
        num_regions=anime_simulcast_region_counts[stats[0].anime_id],
        is_licensed=stats[0].anime_id in licensed_anime,
        multiplier=1,
    )

    # Haruhi is owned by <= 3% of teams, so watching and completed score is doubled
    assert stats[1].score == 7.96
    assert stats[1].favorites == 14683
    assert stats[1].anime_id == 849
    assert stats[1].total_points == total_points_function(
        stats=stats[1],
        num_regions=anime_simulcast_region_counts[stats[1].anime_id],
        is_licensed=stats[1].anime_id in licensed_anime,
        multiplier=2,
    )

    assert stats[2].dropped == 17066
    assert stats[2].forum_posts == 0
    assert stats[2].anime_id == 30276
    assert stats[2].total_points == total_points_function(
        stats=stats[2],
        num_regions=anime_simulcast_region_counts[stats[2].anime_id],
        is_licensed=stats[2].anime_id in licensed_anime,
        multiplier=1,
    )


@vcr.use_cassette(f"{vcrpath}/anime_stats/get_forum_posts.yaml")
def test_get_forum_posts(orm_anime_factory, config_functor, anime_stats_factory, session):
    one_punch_man = orm_anime_factory(id=30276, name="One Punch Man")
    anime_stats = anime_stats_factory(current_week=6)
    anime_stats.forum_post_week_interval = 2
    assert anime_stats.get_forum_posts(fal.models.Anime.from_orm_anime(one_punch_man, session)) == 327 + 426

@patch("fal.controllers.anime_stats.AnimeStats._extract_file_contents")
@patch("fal.controllers.anime_stats.config")
@pytest.mark.parametrize(
    "week,is_valid,section",
    [
        ("1", False, "scoring.simulcast"),
        ("5", True, "scoring.simulcast"),
        ("8", False, "scoring.license"),
        ("13", True, "scoring.license"),
    ],
)
def test_is_week_to_calculate(
    # patches
    config_mock, anime_stats_post_init,
    # fixtures
    config_functor,
    # params
    week, is_valid, section, anime_stats_factory):
    anime_stats_post_init = lambda: None
    config_mock.get.side_effect = config_functor(
        sections=["scoring.simulcast", "scoring.license"], kv={"5": 2000, "13": 10000}
    )
    anime_stats = anime_stats_factory(current_week = week)
    assert anime_stats.is_week_to_calculate(section) == is_valid


def test_get_anime_simulcast_region_counts(
    session, orm_season_factory, orm_anime_factory, anime_stats_factory
):

    season = orm_season_factory(id=0, season_of_year="spring", year=2018)
    cowboy_bebop = orm_anime_factory(id=1, name="Cowboy Bebop", season=season)
    haruhi = orm_anime_factory(id=849, name="Suzumiya Haruhi no Yuuutsu", season=season)
    opm = orm_anime_factory(id=30276, name="One Punch Man", season=season)

    anime_stats = anime_stats_factory()
    anime_stats.simulcast_lines = [
            "Cowboy Bebop = simul simul simul simul",
            "Suzumiya Haruhi no Yuuutsu = simul randomstring simul",
            "One Punch Man = simul simul randomstring simul",
    ]
    assert anime_stats.get_anime_simulcast_region_counts(session) == {1: 4, 849: 2, 30276: 3}


def test_get_licensed_anime(
    session, orm_season_factory, orm_anime_factory, anime_stats_factory
):
    season = orm_season_factory(id=0, season_of_year="spring", year=2018)
    cowboy_bebop = orm_anime_factory(id=1, name="Cowboy Bebop", season=season)
    haruhi = orm_anime_factory(id=849, name="Suzumiya Haruhi no Yuuutsu", season=season)
    opm = orm_anime_factory(id=30276, name="One Punch Man", season=season)

    anime_stats = anime_stats_factory()
    anime_stats.licenses_lines = ["Suzumiya Haruhi no Yuuutsu", "One Punch Man"]
    assert anime_stats.get_licensed_anime(session) == {849, 30276}
