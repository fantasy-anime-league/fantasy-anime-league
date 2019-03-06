#!/usr/bin/python3.7
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

import argparse

parser = argparse.ArgumentParser(
    description="Run the Fantasy Anime League Engine")
parser.add_argument("--collect-series", action="store_true")
parser.add_argument("--ptw-counter", action="store_true")
args = parser.parse_args()


if args.collect_series:
    fal.collect_series.collect_series()
elif args.ptw_counter:
    fal.ptw_counter.ptw_counter()
