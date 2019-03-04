# -*- coding: utf-8 -*-

# run_fal.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)


import fal.details
import fal.ranking_overview
import fal.results
import fal.scorer
import fal.teams
import fal.weekly_performance
import fal.funcs

# True = get new data (default) | False = get existing data
# fal.scorer.main()
# fal.results.main()
# fal.details.main()

# teams.banner_data()

# these functions have been broken for a while... need to be fixed
# weekly_performance.main()
# ranking_overview.main()

# functions for the registration
fal.teams.create_teams()
fal.teams.headcount("Fall", "2018")

# generate statistics
fal.teams.team_overview()
fal.teams.team_stats(True)
fal.teams.team_dist(True)
