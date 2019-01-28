# -*- coding: utf-8 -*-
# funcs.py
# contains (global) help functions
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)

import os
import pickle
import re
import zipfile

# ----------------------------------------------------------------------------
# DATA SAVE/LOAD FUNCTIONS
# ----------------------------------------------------------------------------

# loads data files (pickles)
def load_data(date, zip_file, f_name):
    return pickle.loads(zip_file.read("week_%.2d_%s" % (date, f_name)))

# gets dump string of a pickle and adds to zip archive
def save_data(obj, date, zip_file, f_name):
    dump_string = pickle.dumps(obj)
    zip_file.writestr("week_%.2d_%s" % (date, f_name), dump_string)

# saves all data structures for the given date (week)
def save_all_data(date, teams, swaps, aces, wildcards, anime, a_scores, t_scores, retrieve=True):
    path = "data/"
    if retrieve:
        location = "%sweek_%.2d.zip" % (path, date)
    else:
        location = "%sweek_%.2d_new.zip" % (path, date)
    if os.access(location, os.F_OK):
        return

    # change names back to initial names

    name_changes = map_users()
    for initial, new in list(name_changes.items()):
        current_name = new[-1]
        teams[initial] = teams.pop(current_name)
        swaps[initial] = swaps.pop(current_name)
        aces[initial] = aces.pop(current_name)
        wildcards[initial] = wildcards.pop(current_name)
        t_scores[initial] = t_scores.pop(current_name)

    zip_file = zipfile.ZipFile(location, "w")
    save_data(teams, date, zip_file, "teams")
    save_data(swaps, date, zip_file, "swaps")
    save_data(aces, date, zip_file, "aces")
    save_data(wildcards, date, zip_file, "wildcards")
    save_data(anime, date, zip_file, "anime")
    save_data(a_scores, date, zip_file, "a_scores")
    save_data(t_scores, date, zip_file, "t_scores")
    zip_file.close()

# loads all data structures for the given date (week)
# returns data structures
def load_all_data(date):
    path = "data/"
    location = "%sweek_%.2d.zip" % (path, date)
    zip_file = zipfile.ZipFile(location, "r")
    teams = load_data(date, zip_file, "teams")
    swaps = load_data(date, zip_file, "swaps")
    aces = load_data(date, zip_file, "aces")
    wildcards = load_data(date, zip_file, "wildcards")
    anime = load_data(date, zip_file, "anime")
    a_scores = load_data(date, zip_file, "a_scores")
    t_scores = load_data(date, zip_file, "t_scores")

    # check for name changes
    name_changes = map_users()
    for team in name_changes:
        current_name = name_changes[team][-1]
        teams[current_name] = teams.pop(team)
        swaps[current_name] = swaps.pop(team)
        aces[current_name] = aces.pop(team)
        wildcards[current_name] = wildcards.pop(team)
        t_scores[current_name] = t_scores.pop(team)

    return (teams, swaps, aces, wildcards, anime, a_scores, t_scores)


# returns a writer (for results) to the corresponding path
def open_out_file(week, f_name):
    path = "results/"
    location = "%sweek_%.2i_%s.txt" % (path, week, f_name)
    if not os.access(location, os.F_OK):
        return open("%s" % location, "w")


# ----------------------------------------------------------------------------
# DATA MAPPING FUNCTIONS
# ----------------------------------------------------------------------------

# creates {title:ID} mapping for anime
def map_anime():
    path = "lists/"
    return {a_title.strip(): a_id for a_id, a_title in re.findall(r'(\d+)\s(.+)', open("%sanime_list.txt" % path).read())}

# creates {initial:[new]} mapping for usernames
def map_users():
    path = "lists/"
    return {n[0]: n[1:] for n in [n.split() for n in open("%sname_changes.txt" % path).readlines()]}

# returns string of old names
def get_old_names(current_name, inv_name_changes):
    if current_name not in inv_name_changes:
        return ""
    else:
        return " (%s)" % ", ".join(inv_name_changes[current_name])


# ----------------------------------------------------------------------------
# SPELLING CORRECTION FUNCTIONS
# ----------------------------------------------------------------------------

# {{{ http://code.activestate.com/recipes/576874/ (r1)
def levenshtein(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    matrix = [list(range(l1 + 1))] * (l2 + 1)
    for zz in range(l2 + 1):
        matrix[zz] = list(range(zz, zz + l1 + 1))
    for zz in range(0, l2):
        for sz in range(0, l1):
            if s1[sz] == s2[zz]:
                matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
            else:
                matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
    return matrix[l2][l1]

# dist >4: matches correct titles wrongly! (e.g. zetman gon)
def spelling_correction(wrong_title):
    max_dist = 2
    for a_title in map_anime():
        dist = levenshtein(wrong_title.lower(), a_title.lower())
        if dist <= max_dist:
            return a_title
    return ""

# determines the maximum dist (avoid matching correct titles wrongly)
def find_max_dist():
    tmp_dist = 6
    output_file = open("lev.txt", "w")
    for x in map_anime():
        for y in map_anime():
            dist = levenshtein(x.lower(), y.lower())
            if dist < tmp_dist and dist != 0:
                output_file.write("%s %s %s\n" % (dist, x.lower(), y.lower()))
    output_file.close()
