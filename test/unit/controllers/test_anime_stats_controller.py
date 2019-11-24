from unittest.mock import patch
import configparser
import pytest
import vcr
import factory

from fal.controllers import anime_stats
from fal.orm import AnimeWeeklyStat, Anime, Season

config = configparser.ConfigParser()
config.read("config.ini")


vcrpath = config.get("vcr", "path")

DROPPED_POINTS = -4
SIMULCAST_POINTS = 2000
LICENSE_POINTS = 10000


def total_points_with_dropped(stats, i, num_regions, is_licensed, multiplier):
    return (
        multiplier * (stats[i].watching + stats[i].completed)
        + DROPPED_POINTS * stats[i].dropped
    )


def total_points_with_simulcast(stats, i, num_regions, is_licensed, multiplier):
    return (
        multiplier * (stats[i].watching + stats[i].completed)
        + SIMULCAST_POINTS * num_regions
    )


def total_points_with_license(stats, i, num_regions, is_licensed, multiplier):
    return multiplier * (stats[i].watching + stats[i].completed) + (
        LICENSE_POINTS if is_licensed else 0
    )


@patch("fal.controllers.anime_stats.get_forum_posts")
@patch("fal.controllers.anime_stats.config")
@patch("fal.controllers.anime_stats.session_scope")
@vcr.use_cassette(f"{vcrpath}/anime_stats/populate_anime_weekly_stats.yaml")
@pytest.mark.parametrize(
    "week,points,total_points_function,section",
    [
        ("4", DROPPED_POINTS, total_points_with_dropped, "scoring.dropped"),
        ("5", SIMULCAST_POINTS, total_points_with_simulcast, "scoring.simulcast"),
        ("13", LICENSE_POINTS, total_points_with_license, "scoring.license"),
    ],
)
def test_populate_anime_weekly_stats(
    session_scope_mock,
    config_mock,
    get_forum_posts,
    session_scope,
    config_functor,
    season_factory,
    anime_factory,
    team_factory,
    team_weekly_anime_factory,
    week,
    points,
    total_points_function,
    section,
):
    session_scope_mock.side_effect = session_scope
    config_function = config_functor(
        sections=["season info", "weekly info", "jikanpy", "scoring info", section],
        kv={
            "season": "spring",
            "year": 2018,
            "current-week": week,
            "forum-posts-every-n-weeks": 2,
            "forum-post-multiplier": 25,
            "request-interval": 0,
            "percent-ownership-for-double-score": 3,
            week: points,
        },
    )
    config_mock.getint.side_effect = config_function
    config_mock.get.side_effect = config_function

    get_forum_posts.return_value = 0

    season = season_factory(id=0, season_of_year="spring", year=2018)
    cowboy_bebop = anime_factory(id=1, name="Cowboy Bebop", season=season)
    haruhi = anime_factory(id=849, name="Suzumiya Haruhi no Yuuutsu", season=season)
    opm = anime_factory(id=30276, name="One Punch Man", season=season)

    # Only 1 out of 34 teams owns Haruhi, which is <= 3%
    teams = team_factory.create_batch(34, season=season)
    team_weekly_anime_factory(team=teams[0], anime=cowboy_bebop, week=week)
    team_weekly_anime_factory(team=teams[0], anime=haruhi, week=week)
    for team in teams[1:]:
        team_weekly_anime_factory(team=team, anime=cowboy_bebop, week=week)
        team_weekly_anime_factory(team=team, anime=opm, week=week)

    simulcast_lines = [
        "Cowboy Bebop = simul simul simul simul",
        "Suzumiya Haruhi no Yuuutsu = simul randomstring simul",
        "One Punch Man = simul simul randomstring simul",
    ]
    anime_simulcast_region_counts = {1: 4, 849: 2, 30276: 3}
    licenses_lines = ["Suzumiya Haruhi no Yuuutsu", "One Punch Man"]
    licensed_anime = {849, 30276}

    anime_stats.populate_anime_weekly_stats(simulcast_lines, licenses_lines)
    with session_scope() as session:
        stats = session.query(AnimeWeeklyStat).order_by(AnimeWeeklyStat.anime_id).all()

    assert len(stats) == 3

    print(stats)
    assert stats[0].watching == 71944
    assert stats[0].completed == 526969
    assert stats[0].anime_id == 1
    assert stats[0].total_points == total_points_function(
        stats,
        i=0,
        num_regions=anime_simulcast_region_counts[stats[0].anime_id],
        is_licensed=stats[0].anime_id in licensed_anime,
        multiplier=1,
    )

    # Haruhi is owned by <= 3% of teams, so watching and completed score is doubled
    assert stats[1].score == 7.96
    assert stats[1].favorites == 14683
    assert stats[1].anime_id == 849
    assert stats[1].total_points == total_points_function(
        stats,
        i=1,
        num_regions=anime_simulcast_region_counts[stats[1].anime_id],
        is_licensed=stats[1].anime_id in licensed_anime,
        multiplier=2,
    )

    assert stats[2].dropped == 17066
    assert stats[2].forum_posts == 0
    assert stats[2].anime_id == 30276
    assert stats[2].total_points == total_points_function(
        stats,
        i=2,
        num_regions=anime_simulcast_region_counts[stats[2].anime_id],
        is_licensed=stats[2].anime_id in licensed_anime,
        multiplier=1,
    )


@patch("fal.controllers.anime_stats.config")
@vcr.use_cassette(f"{vcrpath}/anime_stats/get_forum_posts.yaml")
def test_get_forum_posts(config_mock, anime_factory, config_functor, session):
    config_mock.getint.side_effect = config_functor(
        sections=["weekly info", "scoring info"],
        kv={"current-week": 6, "forum-posts-every-n-weeks": 2},
    )
    one_punch_man = anime_factory(id=30276, name="One Punch Man")
    assert anime_stats.get_forum_posts(one_punch_man) == 327 + 426


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
def test_is_week_to_calculate(config_mock, config_functor, week, is_valid, section):
    config_mock.get.side_effect = config_functor(
        sections=["scoring.simulcast", "scoring.license"], kv={"5": 2000, "13": 10000}
    )
    assert anime_stats.is_week_to_calculate(section, week) == is_valid


@patch("fal.controllers.anime_stats.session_scope")
def test_get_anime_simulcast_region_counts(
    session_scope_mock, session_scope, season_factory, anime_factory
):
    session_scope_mock.side_effect = session_scope

    season = season_factory(id=0, season_of_year="spring", year=2018)
    cowboy_bebop = anime_factory(id=1, name="Cowboy Bebop", season=season)
    haruhi = anime_factory(id=849, name="Suzumiya Haruhi no Yuuutsu", season=season)
    opm = anime_factory(id=30276, name="One Punch Man", season=season)

    assert anime_stats.get_anime_simulcast_region_counts(
        [
            "Cowboy Bebop = simul simul simul simul",
            "Suzumiya Haruhi no Yuuutsu = simul randomstring simul",
            "One Punch Man = simul simul randomstring simul",
        ]
    ) == {1: 4, 849: 2, 30276: 3}


@patch("fal.controllers.anime_stats.session_scope")
def test_get_licensed_anime(
    session_scope_mock, session_scope, season_factory, anime_factory
):
    session_scope_mock.side_effect = session_scope

    season = season_factory(id=0, season_of_year="spring", year=2018)
    cowboy_bebop = anime_factory(id=1, name="Cowboy Bebop", season=season)
    haruhi = anime_factory(id=849, name="Suzumiya Haruhi no Yuuutsu", season=season)
    opm = anime_factory(id=30276, name="One Punch Man", season=season)

    assert anime_stats.get_licensed_anime(
        ["Suzumiya Haruhi no Yuuutsu", "One Punch Man"]
    ) == {849, 30276}
