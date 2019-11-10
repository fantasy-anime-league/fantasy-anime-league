from __future__ import annotations

import configparser
from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from fal.clients.mfalncfm_main import session_scope
from fal.orm import TeamWeeklyAnime, Team, Season, Anime

config = configparser.ConfigParser()
config.read("config.ini")


def ace_already_loaded_this_week(team: Team, week: int, session: Session) -> bool:
    """Checks if a team has already aced an anime this week.
    Raises exception if multiple anime has been aced on this team.
    """
    this_week_team_aced_anime = (
        session.query(TeamWeeklyAnime)
        .filter(
            TeamWeeklyAnime.team_id == team.id,
            TeamWeeklyAnime.week == week,
            TeamWeeklyAnime.ace == 1,
        )
        .all()
    )

    assert (
        len(this_week_team_aced_anime) < 2
    ), f"somehow two anime ({this_week_team_aced_anime}) got aced on this team this week: {team}"
    return len(this_week_team_aced_anime) == 1


def team_anime_aced_already(team: Team, anime: Anime, session: Session) -> bool:
    """Checks if an anime has been aced already in previous weeks.
    Raises exception if an anime has been aced more than once on this team
    """

    aced = (
        session.query(TeamWeeklyAnime)
        .filter(
            TeamWeeklyAnime.anime_id == anime.id,
            TeamWeeklyAnime.team_id == team.id,
            TeamWeeklyAnime.ace == 1,
        )
        .all()
    )
    assert (
        len(aced) < 2
    ), f"somehow an anime ({anime}) got aced twice on this team: {team}"
    return len(aced) == 1


def load_aces(input_lines: Iterable[str]) -> None:
    """Takes in an iterable of "<teamname> <anime to ace>" inputs.
    Parses these inputs and sets the anime for the team to ace for the week
    if the anime has not been previously aced on that team and the score for that anime hasn't hit the cutoff.
    """

    season_of_year = config.get("season info", "season").lower()
    year = config.getint("season info", "year")
    week = config.getint("weekly info", "current-week")

    with session_scope() as session:
        season = Season.get_season_from_database(season_of_year, year, session)
        for line in input_lines:
            teamname, animename = line.split(" ", 1)
            team = Team.get_team_from_database(teamname, season, session)
            anime = Anime.get_anime_from_database_by_name(animename.strip(), session)
            assert anime
            if not team_anime_aced_already(team, anime, session):
                this_week_team_anime = (
                    session.query(TeamWeeklyAnime)
                    .filter(
                        TeamWeeklyAnime.anime_id == anime.id,
                        TeamWeeklyAnime.team_id == team.id,
                        TeamWeeklyAnime.week == week,
                    )
                    .one()
                )
                if ace_already_loaded_this_week(team, week, session):
                    print(
                        f"{team.name} tried to ace {anime.name}, but already has an anime aced this week"
                    )
                elif this_week_team_anime.bench == 1:
                    print(f"{team.name} tried to ace {anime.name}, but it was benched")
                else:
                    this_week_team_anime.ace = 1

            else:
                print(
                    f"{team.name} tried to ace {anime.name}, but it has already been aced"
                )
