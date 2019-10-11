from __future__ import annotations

import configparser

from sqlalchemy.sql import func, desc

from fal.clients.mfalncfm_main import session_scope
from fal.models import TeamWeeklyPoints, Season, TeamWeeklyAnime, AnimeWeeklyStat

from typing import TYPE_CHECKING, List, Tuple, Optional, Any, Iterable

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from fal.models import Team

config = configparser.ConfigParser()
config.read("config.ini")


def already_got_high_bonus(team_id: int, session: Session) -> bool:
    query = session.query(TeamWeeklyPoints).filter(
        TeamWeeklyPoints.is_highest == 1, TeamWeeklyPoints.team_id == team_id
    )

    return query.count() > 0


def get_team_scores_counts_this_week(
    week: int, session: Session
) -> List[Tuple[int, int]]:
    """
    Retrieve all team scores this week along with their counts grouped by team score,
    (in other words, how often each numerical team score happened this week)
    ordered by team score descending

    Returns a list of <Count, Teamid> pairs, where TeamId is probably only relevant
    if Count == 1 (otherwise it'll be a random Teamid that matches)
    """

    return (
        session.query(
            func.count(TeamWeeklyPoints.weekly_points), TeamWeeklyPoints.team_id
        )
        .filter(TeamWeeklyPoints.week == week)
        .group_by(TeamWeeklyPoints.weekly_points)
        .order_by(desc(TeamWeeklyPoints.weekly_points))
        .all()
    )


def calculate_team_total_score(team: Team, session: Session) -> int:
    return (
        session.query(func.sum(TeamWeeklyPoints.weekly_points))
        .filter(TeamWeeklyPoints.team_id == team.id)
        .scalar()
    )


def add_team_anime_scores_and_ace_to_weekly_points(
    this_week_points: TeamWeeklyPoints, session: Session
) -> None:
    ace_cutoff = config.getint("scoring info", "ace-cutoff")
    ace_value = config.getint("scoring info", "ace-value")

    active_anime_stats = (
        session.query(TeamWeeklyAnime, AnimeWeeklyStat)
        .filter(
            TeamWeeklyAnime.week == this_week_points.week,
            TeamWeeklyAnime.bench == 0,
            TeamWeeklyAnime.team_id == this_week_points.team_id,
            TeamWeeklyAnime.anime_id == AnimeWeeklyStat.anime_id,
        )
        .order_by(desc(AnimeWeeklyStat.total_points))
        .all()
    )

    this_week_points.weekly_points = sum(
        stat.AnimeWeeklyStat.total_points for stat in active_anime_stats
    )

    assert this_week_points.weekly_points is not None

    top_scoring_anime_on_team = True
    for team_weekly_anime, anime_weekly_stat in active_anime_stats:
        if team_weekly_anime.ace:
            print(
                f"{team_weekly_anime.team.name} attempted to ace {team_weekly_anime.anime.name}, "
            )
            if anime_weekly_stat.watching + anime_weekly_stat.completed > ace_cutoff:
                print("but is over the cutoff")
            elif top_scoring_anime_on_team:
                print(f"and earned an extra {ace_value}")
                this_week_points.weekly_points += ace_value
            else:
                print(
                    f"but lost {ace_value} because it's not the highest scoring eligible anime"
                )
                this_week_points.weekly_points -= ace_value
            break
        elif anime_weekly_stat.watching + anime_weekly_stat.completed < ace_cutoff:
            top_scoring_anime_on_team = False


def calculate_team_scores() -> None:
    """
    For every team "this week" in this season, calculate its points based on
    the criteria of the week.
    """

    season_of_year = config.get("season info", "season").lower()
    year = config.getint("season info", "year")
    week = config.getint("weekly info", "current-week")

    with session_scope() as session:
        teams = Season.get_season_from_database(season_of_year, year, session).teams

        assert isinstance(teams, list)
        for team in teams:
            this_week_points = TeamWeeklyPoints(team_id=team.id, week=week)
            session.add(this_week_points)
            add_team_anime_scores_and_ace_to_weekly_points(this_week_points, session)
            this_week_points.total_points = calculate_team_total_score(team, session)

        for count, team_id in get_team_scores_counts_this_week(week, session):
            if count == 1 and not already_got_high_bonus(team_id, session):
                top_unique_awarded = (
                    session.query(TeamWeeklyPoints)
                    .filter(
                        TeamWeeklyPoints.week == week,
                        TeamWeeklyPoints.team_id == team_id,
                    )
                    .one()
                )

                top_unique_awarded.weekly_points += config.getint(
                    "scoring info", "highest-unique"
                )
                top_unique_awarded.total_points += config.getint(
                    "scoring info", "highest-unique"
                )
                top_unique_awarded.is_highest = 1
                break

    # TODO: deal with wildcards
