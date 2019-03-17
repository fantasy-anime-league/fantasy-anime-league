from __future__ import annotations

from typing import Sequence, List, TYPE_CHECKING
import configparser
import dataclasses

from fal.clients.mfalncfm_main import session_scope
from fal.models import Team, Anime, Season, TeamWeeklyAnime

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


@dataclasses.dataclass
class TeamLines():
    teamname: str
    active: List[str]
    bench: List[str]


config = configparser.ConfigParser()
config.read("config.ini")


def slice_up_team_input(team_lines: Sequence[str]) -> TeamLines:
    """ Take in a block of lines from the registration file,
    break it up into 3 distinct sections:
    Teamname, Active Anime, and Bench Anime

    Return these sections in a namedtuple TeamTuple
    """

    active_len = config['season info']['num-active-on-team']
    bench_len = config['season info']['num-on-bench']

    # teamname + main team + bench
    assert len(team_lines) == active_len + bench_len + 1

    return TeamTuple(team_lines[0], team_lines[1: active_len], team_lines[-bench_len])


def add_anime_to_team(team: Team, anime_lines: List[str], bench: bool, session: Session) -> None:
    for anime_name in anime_lines:
        anime = Anime.get_anime_from_database_by_name(anime_name, session)
        team_weekly_anime = TeamWeeklyAnime(
            team_id=team.id,
            anime_id=anime.id,
            week=1,
            bench=bench
        )
        session.add(team_weekly_anime)


def load_teams(registration_file: str) -> None:
    assert config['weekly info']['current-week'] <= 1, "Cannot add teams after week 1"

    with open(registration_file) as f:
        registration_data = f.readlines()

    with session_scope() as session:
        current_season = Season.get_season_from_database(
            config['season info']['season'], config['season info']['year'], session)

        team_lines = []
        for line_num, line in enumerate(registration_data, 1):
            if line.strip() == "":
                assert team, f"Hit a line of whitespace at line {line_num} but no team was assembled"
                teamtuple = slice_up_team_input(team)
                team = Team.get_team_from_database(
                    teamtuple.teamname, current_season, session)
                add_anime_to_team(team, teamtuple.active, False, session)
                add_anime_to_team(team, teamtuple.bench, True, session)
                team_lines = []
            else:
                team_lines.append(line)
