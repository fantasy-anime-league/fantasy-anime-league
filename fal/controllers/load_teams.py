from __future__ import annotations

import configparser
import dataclasses
import time
from dateutil.parser import parse
from typing import Sequence, List, TYPE_CHECKING, cast, Iterable

import jikanpy

from fal.clients.mfalncfm_main import session_scope
from fal.orm import Team, Anime, Season, TeamWeeklyAnime

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


@dataclasses.dataclass(frozen=True)
class TeamLines:
    teamname: str
    active: Sequence[str]
    bench: Sequence[str]


config = configparser.ConfigParser()
config.read("config.ini")


def slice_up_team_input(team_input: Sequence[str]) -> TeamLines:
    """ Take in a block of lines from the registration file,
    break it up into 3 distinct sections:
    Teamname, Active Anime, and Bench Anime

    Parse out the teamname as well

    Return these sections in a TeamLines object
    """

    active_len = config.getint("season info", "num-active-on-team")
    bench_len = config.getint("season info", "num-on-bench")

    # teamname + main team + bench
    assert len(team_input) == active_len + bench_len + 1
    assert team_input[0][:6].strip() == "Team:", f"Team line: {team_input[0]}"

    return TeamLines(
        team_input[0][6:].strip(),
        team_input[1 : 1 + active_len],
        team_input[-1 * bench_len :],
    )


def add_anime_to_team(
    team: Team, anime_lines: Sequence[str], bench: int, session: Session
) -> None:
    """Add anime by name to the team in the database.
       Raises an exception if anime cannot be found in database
       """

    for anime_name in anime_lines:
        anime_name = anime_name.strip()
        anime = Anime.get_anime_from_database_by_name(anime_name, session)
        if not anime:
            print(
                f"{team.name} has {anime_name} on their team,"
                " which is not in the database"
            )
            return

        assert anime.season_id == team.season_id
        if not anime.eligible:
            print(
                f"{team.name} has {anime_name} on their team,"
                " which is not eligible for this season"
            )

        team_weekly_anime = TeamWeeklyAnime(
            team_id=team.id, anime_id=anime.id, week=0, bench=bench
        )
        session.merge(team_weekly_anime)


def load_teams(registration_data: Sequence[str]) -> None:
    """Takes the contents of registration.txt (read into a list already) and marshalls them into the database"""

    assert (
        config.getint("weekly info", "current-week") <= 1
    ), "Cannot add teams after week 1"

    # group the contents of the input registration file into separate teams,
    # loaded into TeamLines objects
    accumulated_team_input: List[str] = []
    team_lines_list: List[TeamLines] = []
    for line_num, line in enumerate(registration_data, 1):
        if line.strip() == "":
            assert (
                accumulated_team_input
            ), f"Hit a line of whitespace at line {line_num} but no team was assembled"
            team_lines_list.append(slice_up_team_input(accumulated_team_input))
            accumulated_team_input = []
        else:
            accumulated_team_input.append(line)

    # one more time in case we don't have a trailing whitespace line
    if accumulated_team_input:
        team_lines_list.append(slice_up_team_input(accumulated_team_input))

    # take the TeamLines objects and load them into the database
    with session_scope() as session:
        current_season = Season.get_season_from_database(
            config["season info"]["season"],
            config.getint("season info", "year"),
            session,
        )

        for team_lines in team_lines_list:
            print(f"Adding {team_lines.teamname} to database")
            team = Team.get_team_from_database(
                team_lines.teamname, current_season, session
            )
            add_anime_to_team(team, team_lines.active, 0, session)
            add_anime_to_team(team, team_lines.bench, 1, session)


def team_ages() -> None:
    """
    Potentially can help spot alt accounts
    """
    jikan = jikanpy.Jikan()
    season_of_year = config.get("season info", "season")
    year = config.getint("season info", "year")

    with session_scope() as session:
        teams = Season.get_season_from_database(season_of_year, year, session).teams
        for team in cast(Iterable[Team], teams):
            if not team.mal_join_date:
                print(f"Getting join date for {team.name}")
                assert team.name
                try:
                    team.mal_join_date = parse(jikan.user(team.name)["joined"])
                    session.commit()
                    # time.sleep(config.get('jikanpy', 'request-interval'))
                except Exception as e:
                    print(
                        f"Ran into issues figuring out join date with {team.name}: {str(e)}"
                    )
                    continue
