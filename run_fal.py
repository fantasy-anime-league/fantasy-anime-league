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
from fal.controllers.load_teams import load_teams
from fal.controllers.anime_stats import populate_anime_weekly_stats
from fal.views.teams import headcount, team_overview, team_stats, team_dist

import argparse
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
season_str: str = config["season info"]["season"]
year: int = config.getint("season info", "year")

parser = argparse.ArgumentParser(
    description="Run the Fantasy Anime League Engine")
parser.add_argument("--collect-series", action="store_true")
parser.add_argument("--ptw-counter", action="store_true")
parser.add_argument("--load-teams", action="store_true")
parser.add_argument("--registration-file", default="registration.txt")
parser.add_argument("--headcount", action="store_true")
parser.add_argument("--team-overview", action="store_true")
parser.add_argument("--team-stats", action="store_true")
parser.add_argument("--team-dist", action="store_true")
parser.add_argument("--anime-weekly-stats", action="store_true")
parser.add_argument("--season", default=season_str)
parser.add_argument("--year", default=year)
args = parser.parse_args()


if args.collect_series:
    collect_series()
elif args.ptw_counter:
    ptw_counter()
elif args.load_teams:
    with open(args.registration_file, encoding='utf-8-sig') as f:
        registration_data = f.readlines()
    load_teams(registration_data)
elif args.headcount:
    headcount(args.season, args.year)
elif args.team_overview:
    team_overview(args.season, args.year)
elif args.team_stats:
    team_stats(args.season, args.year)
elif args.team_dist:
    team_dist(args.season, args.year)
elif args.anime_weekly_stats:
    populate_anime_weekly_stats()
