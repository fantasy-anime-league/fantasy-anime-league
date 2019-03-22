# -*- coding: utf-8 -*-

# run_fal.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)


import oldfal.details
import oldfal.ranking_overview
import oldfal.results
import oldfal.scorer
import oldfal.teams
import oldfal.weekly_performance
import oldfal.funcs

# True = get new data (default) | False = get existing data
# oldfal.scorer.main()
# oldfal.results.main()
# oldfal.details.main()

# teams.banner_data()

# these functions have been broken for a while... need to be fixed
# weekly_performance.main()
# ranking_overview.main()

# functions for the registration
oldfal.teams.create_teams()
oldfal.teams.headcount("Fall", "2018")

# generate statistics
oldfal.teams.team_overview()
oldfal.teams.team_stats(True)
oldfal.teams.team_dist(True)
