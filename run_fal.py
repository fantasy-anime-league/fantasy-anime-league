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

import argparse

parser = argparse.ArgumentParser(
    description="Run the Fantasy Anime League Engine")
parser.add_argument("--collect-series", action="store_true")
parser.add_argument("--ptw-counter", action="store_true")
parser.add_argument("--load-teams", action="store_true")
parser.add_argument("--registration-file", default="registration.txt")
args = parser.parse_args()


if args.collect_series:
    collect_series()
elif args.ptw_counter:
    ptw_counter()
elif args.load_teams:
    load_teams(args.registration_file)
