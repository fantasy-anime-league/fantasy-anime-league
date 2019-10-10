#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# run_fal.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379

"""
Main file to run Fantasy Anime League Engine. Should replace old_run_fal.py once
it is able to replicate all functionality
"""

from fal.controllers.collect_series import collect_series
from fal.controllers.ptw_counter import ptw_counter
from fal.controllers.load_teams import load_teams, team_ages
from fal.controllers.anime_stats import populate_anime_weekly_stats
from fal.controllers.team_score import calculate_team_scores
from fal.controllers.init_new_week import init_new_team_weekly_anime
from fal.controllers.load_aces import load_aces
from fal.views.teams import headcount, team_overview, team_stats, team_dist

import argparse
import configparser
from typing import List, Optional

config = configparser.ConfigParser()
config.read("config.ini")
season_str: str = config["season info"]["season"]
year: int = config.getint("season info", "year")

parser = argparse.ArgumentParser(description="Run the Fantasy Anime League Engine")
parser.add_argument("--collect-series", action="store_true")
parser.add_argument("--ptw-counter", action="store_true")
parser.add_argument("--load-aces", action="store_true")
parser.add_argument("--ace-file", default="aces.txt")
parser.add_argument("--load-teams", action="store_true")
parser.add_argument("--registration-file", default="registration.txt")
parser.add_argument("--headcount", action="store_true")
parser.add_argument("--team-overview", action="store_true")
parser.add_argument("--team-stats", action="store_true")
parser.add_argument("--team-dist", action="store_true")
parser.add_argument("--team-score", action="store_true")
parser.add_argument("--anime-weekly-stats", action="store_true")
parser.add_argument("--fansubs-file", default="fansubs05.txt")
parser.add_argument("--licenses-file", default="licenses.txt")
parser.add_argument("--init-week", action="store_true")
parser.add_argument("--season", default=season_str)
parser.add_argument("--year", default=year)
args = parser.parse_args()


if args.collect_series:
    collect_series()
if args.ptw_counter:
    ptw_counter()

if args.load_teams:
    with open(args.registration_file, encoding="utf-8-sig") as f:
        registration_data = f.readlines()
    load_teams(registration_data)
    team_ages()
if args.headcount:
    headcount(args.season, args.year)
if args.team_overview:
    team_overview(args.season, args.year)
if args.team_stats:
    team_stats(args.season, args.year)
if args.team_dist:
    team_dist(args.season, args.year)

if args.init_week:
    init_new_team_weekly_anime()
if args.load_aces:
    with open(args.ace_file, encoding="utf-8-sig") as f:
        ace_data = f.readlines()
    load_aces(ace_data)
if args.anime_weekly_stats:
    try:
        with open(args.fansubs_file, encoding="utf-8-sig") as f:
            fansubs_lines: Optional[List[str]] = f.readlines()
    except IOError:
        fansubs_lines = None
    try:
        with open(args.licenses_file, encoding="utf-8-sig") as f:
            licenses_lines: Optional[List[str]] = f.readlines()
    except IOError:
        licenses_lines = None
    populate_anime_weekly_stats(fansubs_lines, licenses_lines)
if args.team_score:
    calculate_team_scores()
