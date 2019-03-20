#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# run_fal2.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379

"""
Main file to run Fantasy Anime League Engine. Should replace run_fal.py once
it is able to replicate all functionality
"""

import fal.collect_series
import fal.ptw_counter

import views.teams

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
parser.add_argument("--headcount", action="store_true")
parser.add_argument("--team-overview", action="store_true")
parser.add_argument("--team-stats", action="store_true")
parser.add_argument("--season", default=season_str)
parser.add_argument("--year", default=year)
args = parser.parse_args()


if args.collect_series:
    fal.collect_series.collect_series()
elif args.ptw_counter:
    fal.ptw_counter.ptw_counter()
elif args.headcount:
    views.teams.headcount(args.season, args.year)
elif args.team_overview:
    views.teams.team_overview(args.season, args.year)
elif args.team_stats:
    views.teams.team_stats(args.season, args.year)
