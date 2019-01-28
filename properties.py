# properties.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)

#-----------------------------------------------------------------------------
# Properties File

# This file contains all properties necessary for running FAL.
# The properties are divided into two parts:
# 1. Properties that have to be changed every week
# 2. Properties that have to be set at the beginning of FAL
# Lines starting with # are comments and will be ignored.
# Please make sure not to mess up the structure.
# Only modify the right side of each equation.
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# Properties that have to be changed every week
#-----------------------------------------------------------------------------

# current week
week = 14

# start post of the swap thread
post_start = 4924

# end post of the swap thread
post_end = 4925

# start page of the swap thread
page_start = 99

# end page of the swap thread
page_end = 99

# delay (in seconds) between MAL server accesses
delay = 1


#-----------------------------------------------------------------------------
# Properties that have to be set at the beginning of FAL
#-----------------------------------------------------------------------------

# Thread ID of the swap thread
a_thread = 2315

# number of maximal players for double points
double_watching = 4

# max number for ace restriction
ace_cutoff = 50000

# additional points {week: points}
week_scores = {3:3000, 7:6000, 10:9000, 14:12000}
week_dropped = {4:4, 8:6, 11:8, 14:10}
week_favorites = {5:25, 8:50, 11:75, 14:75}

# starting week of wildcards
start_wildcards = 9

# weeks for fansub group points
fansub_week = [5]

# week for license points
license_week = 13

# number of active anime
team_len = 5

# number of bench anime
bench_len = 2

# number of available swaps
swap_number = 3

# swaps can be made every X weeks
swap_delay = 3

# number of decimal places (players)
p_num = 3
