from dataclasses import dataclass
import configparser

from fal.clients.mfalncfm_main import session_scope
from fal.models import Team, Season, TeamWeeklyAnime, Anime
from fal.collect_series import get_season_from_database

from typing import Sequence, Dict, TYPE_CHECKING
from sqlalchemy.orm import Session

config = configparser.ConfigParser()
config.read("config.ini")
season_str: str = config["season info"]["season"]
year: int = config.getint("season info", "year")


@dataclass()
class AnimeTeamCount:
    num_teams: int
    num_active: int


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


def get_team_from_season(season_str: str, year: int, session: Session) -> Sequence[Team]:
    season: Season = get_season_from_database(season_str, year, session)
    return session.query(Team).filter(Team.season_id == season.id).all()


def headcount(season_str: str = season_str, year: int = year) -> None:
    """
    Creates a formatted forum post for the headcount thread.
    """
    with session_scope() as session:
        teams: Sequence[Team] = get_team_from_season(season_str, year, session)
        with open("lists/team_headcount.txt", "w", encoding="utf-8") as f:
            f.write(HEADCOUNT_INTRO_TEXT.format(season_str.capitalize(), year))
            for team in sorted(teams, key=lambda t: t.name):
                f.write(f"[b]{team.name}[/b]\n")
            f.write(HEADCOUNT_CONC_TEXT.format(len(teams)))


def team_overview(season_str: str = season_str, year: int = year) -> None:
    """
    Creates a formatted forum post for the team overview thread.
    """
    week: int = config.getint('weekly info', 'current-week')
    with session_scope() as session:
        teams: Sequence[Team] = get_team_from_season(season_str, year, session)
        with open("lists/team_overview.txt", "w", encoding="utf-8") as f:
            f.write(f"Team List - FAL {season_str.capitalize()} {year}\n\n\n")
            for team in sorted(teams, key=lambda t: t.name):
                base_query = session.query(TeamWeeklyAnime, Anime). \
                    filter(TeamWeeklyAnime.team_id == team.id). \
                    filter(TeamWeeklyAnime.anime_id == Anime.id). \
                    filter(TeamWeeklyAnime.week == week)
                active_anime = base_query.filter(
                    TeamWeeklyAnime.bench.is_(False)).all()
                bench_anime = base_query.filter(
                    TeamWeeklyAnime.bench.is_(True)).all()
                f.write(f"{team.name}\n---------------------------------\n")
                # list all active series
                for anime in sorted(active_anime, key=lambda a: a[1].name.lower()):
                    f.write(f"{anime[1].name}\n")
                f.write("\n")
                # list all bench series
                for anime in sorted(bench_anime, key=lambda a: a[1].name.lower()):
                    f.write(f"{anime[1].name}\n")
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
        teams: Sequence[Team] = get_team_from_season(season_str, year, session)
        season: Season = get_season_from_database(season_str, year, session)
        query = session.query(Anime).filter(Anime.season_id == season.id)
        anime_list: Sequence[Anime] = query.all()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(TEAM_STATS_TEXT)
            stats: Dict[int, AnimeTeamCount] = {
                a.id: AnimeTeamCount(0, 0) for a in anime_list}
            for team in teams:
                base_query = session.query(TeamWeeklyAnime). \
                    filter(TeamWeeklyAnime.team_id == team.id). \
                    filter(TeamWeeklyAnime.week == week)
                series: Sequence[TeamWeeklyAnime] = base_query.all()
                for anime in series:
                    stats[anime.anime_id].num_teams += 1
                    if not anime.bench:
                        stats[anime.anime_id].num_active += 1
            s_all = sorted(
                anime_list, key=lambda a: stats[a.id].num_teams, reverse=True)
            for n, a in enumerate(s_all, 1):
                f.write(
                    f"{n} - {a.name}: {stats[a.id].num_teams} ({stats[a.id].num_active})\n")


# def team_dist(prep=False):
#     """
#     Creates a statistic of the team distribution (how many people and who chose the same team)
#     This function can also be used during the game to obtain the team distribution of the current week.
#     @param prep during the real game (False) or before the game (True)
#     """
#     if not prep:
#         teams, _, _, _, _, _, _ = funcs.load_all_data(WEEK)
#         team_dist_file = open("lists/team_dist_%.2d.txt" % WEEK, "w")
#     else:
#         teams = pickle.load(open("lists/teams.obj"))
#         team_dist_file = open("lists/team_dist.txt", "w")
#     split_teams = {}
#     nonsplit_teams = {}
#     active_teams = {}
#     for team, series in teams.items():
#         s_team = tuple(sorted(series[:TEAM_LEN], key=lambda x: x[1]) +
#                        sorted(series[TEAM_LEN:], key=lambda x: x[1]))
#         n_team = tuple(sorted(series, key=lambda x: x[1]))
#         a_team = tuple(sorted(series[:TEAM_LEN], key=lambda x: x[1]))
#         # add team name to inverse dictionary (key: sorted list of series)
#         if s_team not in split_teams:
#             split_teams[s_team] = []
#         split_teams[s_team].append(team)
#         if n_team not in nonsplit_teams:
#             nonsplit_teams[n_team] = []
#         nonsplit_teams[n_team].append(team)
#         if a_team not in active_teams:
#             active_teams[a_team] = []
#         active_teams[a_team].append(team)

#     same_series_diff_team_dist = 0
#     n_list_non = []
#     for series, team_list in nonsplit_teams.items():
#         if len(team_list) != 1:
#             n_list_non.append((len(team_list), team_list))
#         else:
#             same_series_diff_team_dist += 1
#     same_series_and_team_dist = 0
#     n_list_split = []
#     for series, team_list in split_teams.items():
#         if len(team_list) != 1:
#             n_list_split.append((len(team_list), team_list))
#         else:
#             same_series_and_team_dist += 1
#     teams_with_same_active_team = 0
#     n_list_act = []
#     for series, team_list in active_teams.items():
#         if len(team_list) != 1:
#             n_list_act.append((len(team_list), team_list))
#         else:
#             teams_with_same_active_team += 1

#     team_dist_file.write(
#         "[u]Same 7 series and same active team/bench distribution[/u]\n")
#     team_dist_file.write("Number of unique teams: %i\n\n" %
#                          same_series_and_team_dist)
#     team_dist_file.write("Same team chosen by:\n")
#     team_dist_file.write("[list]")
#     for entry in sorted(n_list_split, key=lambda x: x[0], reverse=True):
#         team_dist_file.write("[*]%s\n" %
#                              (", ".join(sorted(entry[1], key=str.lower))))
#     team_dist_file.write("[/list]\n")
#     team_dist_file.write(
#         "[u]Same 7 series but different active team/bench distribution[/u]\n")
#     team_dist_file.write("Number of unique teams: %i\n\n" %
#                          same_series_diff_team_dist)
#     team_dist_file.write("Same team chosen by:\n")
#     team_dist_file.write("[list]")
#     for entry in sorted(n_list_non, key=lambda x: x[0], reverse=True):
#         team_dist_file.write("[*]%s\n" %
#                              (", ".join(sorted(entry[1], key=str.lower))))
#     team_dist_file.write("[/list]\n")
#     team_dist_file.write(
#         "[u]Same active team (but can have different benched series)[/u]\n")
#     team_dist_file.write("Number of unique active teams: %i\n\n" %
#                          teams_with_same_active_team)
#     team_dist_file.write("Same team chosen by:\n")
#     team_dist_file.write("[list]")
#     for entry in sorted(n_list_act, key=lambda x: x[0], reverse=True):
#         team_dist_file.write("[*]%s\n" %
#                              (", ".join(sorted(entry[1], key=str.lower))))
#     team_dist_file.write("[/list]")
#     team_dist_file.close()
