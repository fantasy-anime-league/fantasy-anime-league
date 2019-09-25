from unittest.mock import patch
import pytest

from fal.controllers import team_score
from fal.models import TeamWeeklyPoints

def test_already_got_high_bonus(team_weekly_points_factory, team_factory, session):
    team = team_factory()
    team_weekly_points_factory(team=team, week=0)
    team_weekly_points_factory(team=team, week=1, is_highest=1)
    team_weekly_points_factory(team=team, week=2)

    assert team_score.already_got_high_bonus(team.id, session)

def test_did_not_get_high_bonus_yet(team_weekly_points_factory, team_factory, session):
    team = team_factory()
    for week in range(4):
        team_weekly_points_factory(team=team, week=week)

    assert not team_score.already_got_high_bonus(team.id, session)

def test_get_team_scores_counts_this_week_returns_score_groups_descending_order_by_score(
    team_weekly_points_factory,
    team_factory,
    session
):
    week = 1
    teams = team_factory.create_batch(9)
    team_weekly_points_factory(week=week, weekly_points=500, team=teams[0])
    team_weekly_points_factory(week=week, weekly_points=2000, team=teams[1])
    team_weekly_points_factory(week=week, weekly_points=2000, team=teams[2])
    team_weekly_points_factory(week=week, weekly_points=1500, team=teams[3])
    team_weekly_points_factory(week=week, weekly_points=3000, team=teams[4])
    team_weekly_points_factory(week=week, weekly_points=1000, team=teams[5])
    team_weekly_points_factory(week=week, weekly_points=1000, team=teams[6])
    team_weekly_points_factory(week=week, weekly_points=1000, team=teams[7])
    team_weekly_points_factory(week=week, weekly_points=1000, team=teams[8])

    score_counts = team_score.get_team_scores_counts_this_week(week, session)

    # 3000 score group
    assert score_counts[0] == (1, teams[4].id)

    # 2000 score group
    assert score_counts[1][0] == 2
    assert score_counts[1][1] in [teams[1].id, teams[2].id]

    # 1500 score group
    assert score_counts[2] == (1, teams[3].id)

    # 1000 score group
    assert score_counts[3][0] == 4
    assert score_counts[3][1] in [teams[5].id, teams[6].id, teams[7].id, teams[8].id]

    # 1500 score group
    assert score_counts[4] == (1, teams[0].id)

def test_calculate_team_total_score(team_weekly_points_factory, team_factory, session):
    team = team_factory()
    team_points_per_week = [100, 1000, 400, 500]
    for week, weekly_points in zip(range(4), team_points_per_week):
        team_weekly_points_factory(team=team, week=week, weekly_points=weekly_points)

    assert team_score.calculate_team_total_score(team, session) == sum(team_points_per_week)

from fal.models import AnimeWeeklyStat

def test_add_team_anime_scores_to_weekly_points(
    team_weekly_points_factory,
    team_weekly_anime_factory,
    anime_weekly_stat_factory,
    session
):
    this_week_points = team_weekly_points_factory()
    anime_weekly_stats = anime_weekly_stat_factory.create_batch(7)
    bench_anime_stats = anime_weekly_stats[-2:]
    print(bench_anime_stats)
    active_anime_scores = [500, 1000, 1500, 2000, 5000]

    for anime_weekly_stat, anime_score in zip(anime_weekly_stats, active_anime_scores):
        anime_weekly_stat.total_points = anime_score
        team_weekly_anime_factory(
            team = this_week_points.team,
            anime = anime_weekly_stat.anime,
            week = anime_weekly_stat.week
        )

    # bench anime that should not be included in calculations
    for bench_anime_stat in bench_anime_stats:
        bench_anime_stat.total_points = 1
        team_weekly_anime_factory(
            team = this_week_points.team,
            anime = bench_anime_stat.anime,
            week = bench_anime_stat.week,
            bench = 1
        )

    team_score.add_team_anime_scores_to_weekly_points(this_week_points, session)
    assert this_week_points.weekly_points == sum(active_anime_scores)

@patch('fal.controllers.team_score.config')
@patch('fal.controllers.team_score.session_scope')
def test_calculate_team_scores_assigns_highest_team_correctly_and_adds_bonus(
    # patches
    session_scope_mock,
    config_mock,
    #factories
    season_factory,
    team_factory,
    team_weekly_anime_factory,
    anime_weekly_stat_factory,
    #fixtures
    config_functor,
    session_scope,
    session
):
    session_scope_mock.side_effect = session_scope

    config_function = config_functor(
        sections=[
            'season info',
            'weekly info',
            'scoring info',
        ],
        kv={
            'season': 'spring',
            'year': 2018,
            'current-week': 0,
            'highest-unique': 4000
        }
    )
    config_mock.getint.side_effect = config_function
    config_mock.get.side_effect = config_function

    season = season_factory(season_of_year='spring', year=2018)
    teams = team_factory.create_batch(3, season=season)
    anime_weekly_stats = anime_weekly_stat_factory.create_batch(10, week=0)
    anime_scores = list(range(10, 101, 10))

    for anime_weekly_stat, anime_score in zip(anime_weekly_stats, anime_scores):
        anime_weekly_stat.total_points = anime_score

    # set the active anime for each team
    for anime_weekly_stat in anime_weekly_stats[:5]:
        team_weekly_anime_factory(
            team = teams[0],
            anime = anime_weekly_stat.anime,
            week = anime_weekly_stat.week
        )
    for anime_weekly_stat in anime_weekly_stats[3:8]:
        team_weekly_anime_factory(
            team = teams[1],
            anime = anime_weekly_stat.anime,
            week = anime_weekly_stat.week
        )
    for anime_weekly_stat in anime_weekly_stats[-5:]:
        team_weekly_anime_factory(
            team = teams[2],
            anime = anime_weekly_stat.anime,
            week = anime_weekly_stat.week
        )

    team_score.calculate_team_scores()

    top_team = session.query(TeamWeeklyPoints).filter(
        TeamWeeklyPoints.team_id == teams[2].id
    ).one()

    assert top_team.is_highest is 1
    assert top_team.weekly_points == sum(anime_scores[-5:]) + 4000
    assert top_team.total_points == sum(anime_scores[-5:]) + 4000