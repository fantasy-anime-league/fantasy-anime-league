from dataclasses import dataclass
import configparser

from fal.clients.mfalncfm_main import session_scope
from fal.models import Team, Season, TeamWeeklyAnime, Anime

from typing import Dict, Tuple, List, Mapping, Sequence, TextIO, TYPE_CHECKING
from sqlalchemy import func
from sqlalchemy.orm import Session

config = configparser.ConfigParser()
config.read("config.ini")
season_str: str = config["season info"]["season"]
year: int = config.getint("season info", "year")


# Implicitly combined strings for headcount intro and conclusion
HEADCOUNT_INTRO_TEXT = (
    "This is the headcount of the people who have been accepted in Fantasy "
    "Anime League {} {}.\n\n"
)

HEADCOUNT_CONC_TEXT = (
    "\nTotal teams: {}\n\nMake sure to check this list after "
    "registering. We will be regularly updating it so you can see if your team "
    "has been accepted or not.\n\nIf you're not on this list and the post's "
    "last edit time is after you've sent your registration (give or take a few "
    "hours), then you are [b]NOT[/b] registered. In that case, please contact "
    "the FAL staff.\n\nAfter the registration is closed, we'll put up the team "
    "list thread so you can check to make sure your team is correct."
)

TEAM_STATS_TEXT = (
    "[u]Team Stats:[/u]\nThe list is ordered on how many times people chose a "
    "certain anime in their team. The number in the brackets is the amount of "
    "people who have the anime in their active team.\n\n"
)

SAME_SPLIT_TEXT = (
    "[u]Same 7 series and same active team/bench distribution[/u]\nNumber of "
    "unique teams: {}\n\nSame team chosen by:\n[list]"
)

SAME_NONSPLIT_TEXT = (
    "[/list]\n[u]Same 7 series but different active team/bench "
    "distribution[/u]\nNumber of unique teams: {}\n\nSame team chosen by:\n[list]"
)

SAME_ACTIVE_TEXT = (
    "[/list]\n[u]Same active team (but can have different benched series)[/u]"
    "\nNumber of unique active teams: {}\n\nSame team chosen by:\n[list]"
)


def headcount(season_str: str = season_str, year: int = year) -> None:
    """
    Creates a formatted forum post for the headcount thread.
    """
    with session_scope() as session:
        teams = Season.get_season_from_database(
            season_str, year, session).teams
        with open("lists/team_headcount.txt", "w", encoding="utf-8") as f:
            f.write(HEADCOUNT_INTRO_TEXT.format(season_str.capitalize(), year))
            for team in sorted(teams, key=lambda t: t.name):  # type: ignore
                f.write(f"[b]{team.name}[/b]\n")
            f.write(HEADCOUNT_CONC_TEXT.format(len(teams)))  # type: ignore


def team_overview(season_str: str = season_str, year: int = year) -> None:
    """
    Creates a formatted forum post for the team overview thread.
    """
    week: int = config.getint('weekly info', 'current-week')
    with session_scope() as session:
        teams = Season.get_season_from_database(
            season_str, year, session).teams
        with open("lists/team_overview.txt", "w", encoding="utf-8") as f:
            f.write(f"Team List - FAL {season_str.capitalize()} {year}\n\n\n")
            for team in sorted(teams, key=lambda t: t.name):  # type: ignore
                base_query = session.query(TeamWeeklyAnime). \
                    filter(TeamWeeklyAnime.team_id == team.id). \
                    filter(TeamWeeklyAnime.week == week)
                active_anime = base_query.filter(
                    TeamWeeklyAnime.bench.is_(False)).all()
                bench_anime = base_query.filter(
                    TeamWeeklyAnime.bench.is_(True)).all()
                f.write(f"{team.name}\n---------------------------------\n")
                # list all active series
                for anime in sorted(active_anime, key=lambda a: a.anime.name.lower()):
                    f.write(f"{anime.anime.name}\n")
                f.write("\n")
                # list all bench series
                for anime in sorted(bench_anime, key=lambda a: a.anime.name.lower()):
                    f.write(f"{anime.anime.name}\n")
                f.write("\n\n")
            f.write("[/spoiler]")


def team_stats(season_str: str = season_str, year: int = year, prep: bool = True) -> None:
    """
    Creates a statistic of the titles distribution for the team overview thread.
    This function can also be used during the game to obtain the distribution
    of the current week.
    @param prep during the real game (False) or before the game (True)
    """
    week: int = config.getint('weekly info', 'current-week')
    if not prep:
        filename = f"lists/team_stats_{week}.txt"
        raise NotImplementedError("Haven't implemented stats during real game")
    else:
        filename = "lists/team_stats.txt"
    with session_scope() as session:
        season: Season = Season.get_season_from_database(
            season_str, year, session)
        base_query = session.query(Anime.name, func.count('*')). \
            join(TeamWeeklyAnime.anime). \
            order_by(func.count('*').desc(), Anime.name) .\
            filter(TeamWeeklyAnime.week == week)
        anime_counts: List[Tuple[str, int]] = base_query. \
            group_by(Anime.name).all()
        active_counts: Dict[str, int] = dict(base_query.
                                             filter(TeamWeeklyAnime.bench.is_(False)).
                                             group_by(Anime.name).all())
        print(f"Anime Counts:\n{anime_counts}")
        print(f"Active Counts:\n{active_counts}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(TEAM_STATS_TEXT)
            for i, (anime, count) in enumerate(anime_counts, 1):
                active_count = active_counts[anime] if anime in active_counts else 0
                f.write(f"{i} - {anime}: {count} ({active_count})\n")


def team_dist(season_str: str = season_str, year: int = year, prep: bool = True) -> None:
    """
    Creates a statistic of the team distribution (how many people and who chose the same team)
    This function can also be used during the game to obtain the team distribution of the current week.
    @param prep during the real game (False) or before the game (True)
    """
    week: int = config.getint('weekly info', 'current-week')
    if not prep:
        filename = f"lists/team_dist_{week}.txt"
        raise NotImplementedError("Haven't implemented dist during real game")
    else:
        filename = "lists/team_dist.txt"
    split_teams: Dict[Tuple[TeamWeeklyAnime, ...], List[Team]] = {}
    nonsplit_teams: Dict[Tuple[TeamWeeklyAnime, ...], List[Team]] = {}
    active_teams: Dict[Tuple[TeamWeeklyAnime, ...], List[Team]] = {}
    with session_scope() as session:
        teams = Season.get_season_from_database(
            season_str, year, session).teams
        for team in teams:  # type: ignore
            base_query = session.query(TeamWeeklyAnime). \
                filter(TeamWeeklyAnime.team_id == team.id). \
                filter(TeamWeeklyAnime.week == week)
            series: List[TeamWeeklyAnime] = base_query.all()
            active: List[TeamWeeklyAnime] = base_query.filter(
                TeamWeeklyAnime.bench.is_(False)).all()
            bench: List[TeamWeeklyAnime] = base_query.filter(
                TeamWeeklyAnime.bench.is_(True)).all()
            s_team: Tuple[TeamWeeklyAnime, ...] = tuple(sorted(active, key=lambda a: a.anime_id) +
                                                        sorted(bench, key=lambda a: a.anime_id))
            n_team: Tuple[TeamWeeklyAnime, ...] = tuple(
                sorted(series, key=lambda a: a.anime_id))
            a_team: Tuple[TeamWeeklyAnime, ...] = tuple(
                sorted(active, key=lambda a: a.anime_id))
            # add team name to inverse dictionary (key: sorted list of series)
            if s_team not in split_teams:
                split_teams[s_team] = []
            split_teams[s_team].append(team)
            if n_team not in nonsplit_teams:
                nonsplit_teams[n_team] = []
            nonsplit_teams[n_team].append(team)
            if a_team not in active_teams:
                active_teams[a_team] = []
            active_teams[a_team].append(team)

        same_series_diff_team_dist, n_list_non = get_dist(nonsplit_teams)
        same_series_and_team_dist, n_list_split = get_dist(split_teams)
        teams_with_same_active_team, n_list_act = get_dist(active_teams)

        f: TextIO = open(filename, "w", encoding="utf-8")
        write_teams_to_file(f, same_series_and_team_dist,
                            n_list_split, SAME_SPLIT_TEXT)
        write_teams_to_file(f, same_series_diff_team_dist,
                            n_list_non, SAME_NONSPLIT_TEXT)
        write_teams_to_file(f, teams_with_same_active_team,
                            n_list_act, SAME_ACTIVE_TEXT)
        f.write("[/list]")
        f.close()


def write_teams_to_file(f: TextIO, num_unique: int, same_teams: Sequence[Sequence[Team]], output_str: str) -> None:
    f.write(output_str.format(num_unique))
    for team_list in sorted(same_teams, key=lambda t: len(t), reverse=True):
        f.write(
            f"[*]{', '.join([team.name for team in sorted(team_list, key=lambda t: t.name)])}\n")  # type: ignore


def get_dist(teams: Mapping[Tuple[TeamWeeklyAnime, ...], Sequence[Team]]) -> Tuple[int, List[Sequence[Team]]]:
    """Return list of same teams and number of unique teams"""
    same_teams: List[Sequence[Team]] = [
        t for t in teams.values() if len(t) != 1]
    num_unique: int = len(teams) - len(same_teams)
    return num_unique, same_teams
