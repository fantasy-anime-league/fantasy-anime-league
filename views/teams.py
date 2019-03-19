import configparser

from fal.clients.mfalncfm_main import session_scope
from fal.models import Team, Season
from fal.collect_series import get_season_from_database

from typing import Sequence

config = configparser.ConfigParser()
config.read("config.ini")
season_str: str = config["season info"]["season"]
year: int = config.getint("season info", "year")


# Implicitly combined strings for intro and conclusion
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


def headcount(season_str: str = season_str, year: int = year) -> None:
    """
    Creates a formatted forum post for the headcount thread.
    """
    with session_scope() as session:
        season: Season = get_season_from_database(
            season_str.capitalize(), year, session)

        teams: Sequence[Team] = session.query(
            Team).filter(Team.season_id == season.id).all()

        with open("lists/team_headcount.txt", "w", encoding="utf-8") as f:
            f.write(HEADCOUNT_INTRO_TEXT.format(season_str, year))
            for team in sorted(teams, key=lambda team: team.name):
                f.write(f"[b]{team.name}[/b]\n")
            f.write(HEADCOUNT_CONC_TEXT.format(len(teams)))


# def team_overview():
#     """
#     Creates a formatted forum post for the team overview thread.
#     """
#     teams = pickle.load(open("lists/teams.obj"))
#     team_overview_file = open("lists/team_overview.txt", "w")
#     # team_overview_file.write("[u]Team List:[/u]\n[spoiler]\n")
#     team_overview_file.write("Team List - FAL Spring 2016\n\n\n")
#     for team, titles in sorted(teams.items(), key=lambda x: x[0].lower()):
#         # team_overview_file.write("[b][u]%s[/u][/b]\n" % team)
#         team_overview_file.write(
#             "%s\n---------------------------------\n" % team)
#         # list all active series
#         for _, a_title in sorted(titles[:TEAM_LEN], key=lambda x: x[1].lower()):
#             team_overview_file.write("%s\n" % a_title)
#         team_overview_file.write("\n")
#         # list all bench series
#         for _, a_title in sorted(titles[TEAM_LEN:], key=lambda x: x[1].lower()):
#             team_overview_file.write("%s\n" % a_title)
#         team_overview_file.write("\n\n")
#     team_overview_file.write("[/spoiler]")
#     team_overview_file.close()


# def team_stats(prep=False):
#     """
#     Creates a statistic of the titles distribution for the team overview thread.
#     This function can also be used during the game to obtain the distribution
#     of the current week.
#     @param prep during the real game (False) or before the game (True)
#     """
#     if not prep:
#         teams, _, _, _, anime, _, _ = funcs.load_all_data(WEEK)
#         stats_file = open("lists/team_stats_%.2d.txt" % WEEK, "w")
#     else:
#         teams = pickle.load(open("lists/teams.obj"))
#         stats_file = open("lists/team_stats.txt", "w")
#     stats_file.write("[u]Team Stats:[/u]\n")
#     stats_file.write(
#         "The list is ordered on how many times people chose a certain anime ")
#     stats_file.write(
#         "in their team. The number in the brackets is the amount of people ")
#     stats_file.write("who have the anime in their active team.\n\n")
#     anime = re.findall(r'(\d+)\s(.+)', open("lists/anime_list.txt").read())
#     stats = {a_title.strip(): [0, 0] for a_id, a_title in anime}
#     for series in teams.values():
#         for _, a_title in series:
#             stats[a_title][0] += 1
#         for _, a_title in series[:TEAM_LEN]:
#             stats[a_title][1] += 1
#     s_name = sorted(stats.items(), key=lambda x: x[0].lower())
#     s_act = sorted(s_name, key=lambda x: x[1][1], reverse=True)
#     s_all = sorted(s_act, key=lambda x: x[1][0], reverse=True)
#     for n, (a_title, _) in enumerate(s_all):
#         stats_file.write("%i - %s: %i (%i)\n" %
#                          ((n+1), a_title, stats[a_title][0], stats[a_title][1]))
#     stats_file.close()


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
