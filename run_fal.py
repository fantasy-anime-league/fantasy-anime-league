# -*- coding: utf-8 -*-

# fal.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)

import sys

import fal.details
import fal.ranking_overview
import fal.results
import fal.scorer
import fal.teams
import fal.weekly_performance
import fal.funcs

# True = get new data (default) | False = get existing data
fal.scorer.main()

fal.results.main()
fal.details.main()

# teams.banner_data()

# these functions have been broken for a while... need to be fixed
# weekly_performance.main()
# ranking_overview.main()

# functions for the registration
# teams.create_teams()
#teams.headcount("Fall", "2018")

# generate statistics
# teams.team_overview()
# teams.team_stats(True)
# teams.team_dist(True)
