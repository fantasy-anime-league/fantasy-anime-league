# -*- coding: utf-8 -*-
# teams.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)

# ----------------------------------------------------------------------------
# PARAMETERS
# ----------------------------------------------------------------------------

import sys
sys.path.append("../")

import funcs
import properties

import pickle
import re

WEEK = properties.week
TEAM_LEN = properties.team_len
BENCH_LEN = properties.bench_len


# ----------------------------------------------------------------------------
# TEAM FUNCTIONS
# ----------------------------------------------------------------------------

def create_teams():
    """
    Creates the team list used by the scorer program.

    This function reads a list of team + anime titles blocks as they were
    predefined in the registration instructions. It only needs the anime titles
    and adds the corresponding ID that is necessary for the scorer program.

    The function detects errors in the input:
    1. incorrect team length
    2. incorrect titles
    3. double registrations
    4. maximum of sequels (if defined)

    It also creates a teams object with the current teams which can be used by
    other functions in this script.
    """
    mapping = funcs.map_anime()
    sequels = [s.strip() for s in open("lists/sequels.txt").readlines()]
    registration_file = open("registration.txt")
    team_list_file = open("team_list.txt", "w")
    error = False
    teams = {}
    regcount = {}
    inputdata = registration_file.read()
    #all_teams = re.findall('Team: (.+?)\r\n(.+?)\r\n\r\n', inputdata, re.S) # I think I used this under linux
    all_teams = re.findall('Team: (.+?)\n(.+?)\n\n', inputdata, re.S)
    team_errors = re.findall('Username: (.+)', inputdata)
    team_errors.extend(re.findall('Name: (.+)', inputdata))
    for team_error in team_errors:
        print "%s -- team/username error" % (team_error)
    for team, titles in all_teams:
        # allow 1 re-registration
        if team not in regcount:
            regcount[team] = 0
        #print team, regcount[team]
        if team in teams and regcount[team] == 2:
            print "%s (%i) -- no other registration change possible" % (team, regcount[team])
            continue
        series = re.findall('^(.+)$', titles, re.M)
        # check for correct number of titles
        if len(set(series)) != TEAM_LEN + BENCH_LEN:
            print "%s (%i) -- incorrect team length" % (team, regcount[team])
            continue
        # check if all titles are written correctly
        for title in series:
            if title.strip() not in mapping:
                print "%s (%i) -- incorrect title: %s" % (team, regcount[team], title)
                error = True
        if error:
            error = False
            continue
        # check for maximum sequels
        max_sequels = 1
        for title in series:
            if title.strip() in sequels:
                max_sequels -= 1
            if max_sequels < 0:
                print "%s (%i) -- too many sequels" % (team, regcount[team])
                error = True
                break
        if error:
            error = False
            continue
        # only write teams without errors
        regcount[team] += 1
        teams[team] = []
        for title in series:
            teams[team].append((mapping[title.strip()], title.strip()))

    for team, team_list in teams.items():
        team_list_file.write("Team: %s\n" % team)
        for _, title in team_list:
            team_list_file.write("%s %s\n" % (mapping[title.strip()], title.strip()))
        team_list_file.write("\n")
    team_list_file.close()
    pickle.dump(teams, open("lists/teams.obj", "w"))


def headcount(season, year):
    """
    Creates a formatted forum post for the headcount thread.

    @param season the season identifier: Spring or Fall
    @param year the current year
    """
    teams = pickle.load(open("lists/teams.obj"))
    team_headcount_file = open("lists/team_headcount.txt", "w")
    team_headcount_file.write("This is the headcount of the people who have been accepted ")
    team_headcount_file.write("in Fantasy Anime League %s %s.\n\n" % (season, year))
    for team in sorted(teams, key=str.lower):
        team_headcount_file.write("[b]%s[/b]\n" % team)
    team_headcount_file.write("\nTotal teams: %i\n\n" % len(teams))
    team_headcount_file.write("Make sure to check this list after registering. We will be ")
    team_headcount_file.write("regularly updating it so you can see if your team has been ")
    team_headcount_file.write("accepted or not.\n\n")
    team_headcount_file.write("If you're not on this list and the post's last edit time is ")
    team_headcount_file.write("after you've sent your registration (give or take a few hours), then you are [b]NOT[/b] ")
    team_headcount_file.write("registered. In that case, please contact the FAL staff.\n\n")
    team_headcount_file.write("After the registration is closed, we'll put up the team list ")
    team_headcount_file.write("thread so you can check to make sure your team is correct.")
    team_headcount_file.close()


def team_overview():
    """
    Creates a formatted forum post for the team overview thread.
    """
    teams = pickle.load(open("lists/teams.obj"))
    team_overview_file = open("lists/team_overview.txt", "w")
    #team_overview_file.write("[u]Team List:[/u]\n[spoiler]\n")
    team_overview_file.write("Team List - FAL Spring 2016\n\n\n")
    for team, titles in sorted(teams.items(), key=lambda x: x[0].lower()):
        #team_overview_file.write("[b][u]%s[/u][/b]\n" % team)
        team_overview_file.write("%s\n---------------------------------\n" % team)
        # list all active series
        for _, a_title in sorted(titles[:TEAM_LEN], key=lambda x: x[1].lower()):
            team_overview_file.write("%s\n" % a_title)
        team_overview_file.write("\n")
        # list all bench series
        for _, a_title in sorted(titles[TEAM_LEN:], key=lambda x: x[1].lower()):
            team_overview_file.write("%s\n" % a_title)
        team_overview_file.write("\n\n")
    team_overview_file.write("[/spoiler]")
    team_overview_file.close()


def team_stats(prep=False):
    """
    Creates a statistic of the titles distribution for the team overview thread.

    This function can also be used during the game to obtain the distribution
    of the current week.

    @param prep during the real game (False) or before the game (True)
    """
    if not prep:
        teams, _, _, _, anime, _, _ = funcs.load_all_data(WEEK)
        stats_file = open("lists/team_stats_%.2d.txt" % WEEK, "w")
    else:
        teams = pickle.load(open("lists/teams.obj"))
        stats_file = open("lists/team_stats.txt", "w")
    stats_file.write("[u]Team Stats:[/u]\n")
    stats_file.write("The list is ordered on how many times people chose a certain anime ")
    stats_file.write("in their team. The number in the brackets is the amount of people ")
    stats_file.write("who have the anime in their active team.\n\n")
    anime = re.findall(r'(\d+)\s(.+)', open("lists/anime_list.txt").read())
    stats = {a_title.strip(): [0, 0] for a_id, a_title in anime}
    for series in teams.values():
        for _, a_title in series:
            stats[a_title][0] += 1
        for _, a_title in series[:TEAM_LEN]:
            stats[a_title][1] += 1
    s_name = sorted(stats.items(), key=lambda x: x[0].lower())
    s_act = sorted(s_name, key=lambda x: x[1][1], reverse=True)
    s_all = sorted(s_act, key=lambda x: x[1][0], reverse=True)
    for n, (a_title, _) in enumerate(s_all):
        stats_file.write("%i - %s: %i (%i)\n" % ((n+1), a_title, stats[a_title][0], stats[a_title][1]))
    stats_file.close()


def team_dist(prep=False):
    """
    Creates a statistic of the team distribution (how many people and who chose the same team)

    This function can also be used during the game to obtain the team distribution of the current week.

    @param prep during the real game (False) or before the game (True)
    """
    if not prep:
        teams, _, _, _, _, _, _ = funcs.load_all_data(WEEK)
        team_dist_file = open("lists/team_dist_%.2d.txt" % WEEK, "w")
    else:
        teams = pickle.load(open("lists/teams.obj"))
        team_dist_file = open("lists/team_dist.txt", "w")
    split_teams = {}
    nonsplit_teams = {}
    active_teams = {}
    for team, series in teams.items():
        s_team = tuple(sorted(series[:TEAM_LEN], key=lambda x: x[1])+sorted(series[TEAM_LEN:], key=lambda x: x[1]))
        n_team = tuple(sorted(series, key=lambda x: x[1]))
        a_team = tuple(sorted(series[:TEAM_LEN], key=lambda x: x[1]))
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

    same_series_diff_team_dist = 0
    n_list_non = []
    for series, team_list in nonsplit_teams.items():
        if len(team_list) != 1:
            n_list_non.append((len(team_list), team_list))
        else:
            same_series_diff_team_dist += 1
    same_series_and_team_dist = 0
    n_list_split = []
    for series, team_list in split_teams.items():
        if len(team_list) != 1:
            n_list_split.append((len(team_list), team_list))
        else:
            same_series_and_team_dist += 1
    teams_with_same_active_team = 0
    n_list_act = []
    for series, team_list in active_teams.items():
        if len(team_list) != 1:
            n_list_act.append((len(team_list), team_list))
        else:
            teams_with_same_active_team += 1

    team_dist_file.write("[u]Same 7 series and same active team/bench distribution[/u]\n")
    team_dist_file.write("Number of unique teams: %i\n\n" % same_series_and_team_dist)
    team_dist_file.write("Same team chosen by:\n")
    team_dist_file.write("[list]")
    for entry in sorted(n_list_split, key=lambda x: x[0], reverse=True):
        team_dist_file.write("[*]%s\n" % (", ".join(sorted(entry[1], key=str.lower))))
    team_dist_file.write("[/list]\n")
    team_dist_file.write("[u]Same 7 series but different active team/bench distribution[/u]\n")
    team_dist_file.write("Number of unique teams: %i\n\n" % same_series_diff_team_dist)
    team_dist_file.write("Same team chosen by:\n")
    team_dist_file.write("[list]")
    for entry in sorted(n_list_non, key=lambda x: x[0], reverse=True):
        team_dist_file.write("[*]%s\n" % (", ".join(sorted(entry[1], key=str.lower))))
    team_dist_file.write("[/list]\n")
    team_dist_file.write("[u]Same active team (but can have different benched series)[/u]\n")
    team_dist_file.write("Number of unique active teams: %i\n\n" % teams_with_same_active_team)
    team_dist_file.write("Same team chosen by:\n")
    team_dist_file.write("[list]")
    for entry in sorted(n_list_act, key=lambda x: x[0], reverse=True):
        team_dist_file.write("[*]%s\n" % (", ".join(sorted(entry[1], key=str.lower))))
    team_dist_file.write("[/list]")
    team_dist_file.close()


def banner_data():
    """
    Creates input for banner scripts.
    """
    weekly_output_file = open("bannerdata/week%i.txt" % WEEK, "w")
    _, _, _, _, _, _, t_scores = funcs.load_all_data(WEEK)
    for team, scores in sorted(t_scores.items(), key=lambda x: x[1][2]):
        weekly_output_file.write("%s = %i\n" % (team, scores[2]))
    weekly_output_file.close()
