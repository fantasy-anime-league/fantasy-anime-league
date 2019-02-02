# -*- coding: utf-8 -*-
# weekly_performance.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)

# ----------------------------------------------------------------------------
# PARAMETERS
# ----------------------------------------------------------------------------

import funcs
import properties

week = properties.week

# ----------------------------------------------------------------------------
# HELP FUNCTIONS
# ----------------------------------------------------------------------------

# determines algebraic sign; returns no number if 0
def get_sign(number):
  if number > 0:
    return "+%i" % number
  elif number < 0:
    return "%i" % number
  else:
    return "-"

# get weekly team rankings
def get_ranking(w_scores):
  r_scores = {}
  prev = None
  for i, (team, scores) in enumerate(sorted(w_scores.items(), key=lambda x:x[1][0], reverse=True)):
    if scores[0] != prev:
      rank = i + 1
      prev = scores[0]
    r_scores[team] = rank
  return r_scores

# returns a specific number of "whitespaces"
def blank(m, n):
  if m == n:
    return ""
  else:
    return " "*(m-n)

# ----------------------------------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------------------------------

def main():

  ### add old_names in results.py ACES

  ### and what's this? is it necessary to do it here / in funcs.py???????

  ### no name changes in performance/ranking
  ###### but check if current name is there

  # check for name changes
  name_changes = funcs.map_users()
  inv_name_changes = {new[-1]: [initial]+new[:-1] for initial, new in name_changes.items()}

  w = funcs.open_out_file(week, "performances")

  w.write("Weekly Performances; Week %i:\n\n" % week)

  teams, swaps, aces, wildcards, anime, a_scores, t_scores = funcs.load_all_data(week)

  # get team scores WITHOUT aces and wildcards and for active anime only
  clean_t_scores = {team: 0 for team in teams}
  for team in teams:
    for a_id in [a[0] for a in teams[team][:5]]:
      clean_t_scores[team] += a_scores[a_id][1]

  toprank_week = sorted(clean_t_scores.items(), key=lambda x:x[1], reverse=True)[0][0]
  toprank_rank = sorted(t_scores.items(), key=lambda x:x[1][0], reverse=True)[0][0]

  w.write("points this week  (points less than #1 this week)")
  w.write("  [points less than #1 in team ranking]\n\n")
  w_scores = {}
  for team, week_points in sorted(clean_t_scores.items(), key=lambda x:x[1], reverse=True):
    diff_week = week_points - clean_t_scores[toprank_week]
    diff_rank = week_points - clean_t_scores[toprank_rank]
    w_scores[team] = [week_points, get_sign(diff_week), get_sign(diff_rank)]

  ranking = get_ranking(w_scores)
  ranked_teams = {} # {rank: [list of teams]}
  for team, rank in sorted(ranking.items(), key=lambda x:x[1]):
    ranked_teams.setdefault(rank, []).append(team)

  # get length of longest username
  max_name = max([len(team) for team in teams.keys()])
  # get length of highest score
  max_score = max([len(str(score)) for score in clean_t_scores.values()])

  for rank, team_list in sorted(ranked_teams.items()):
    for team in sorted(team_list, key=str.lower):
      w.write("%s%i " % (blank(3,len(str(rank))),rank))
      w.write("%s%s" % (team,blank(max_name,len(team))))
      w.write("%s%i" % (blank(max_score,len(str(w_scores[team][0]))-1),w_scores[team][0]))
      w.write("%s(%s)" % (blank(max_score,len(str(w_scores[team][1]))-3),w_scores[team][1]))
      w.write("%s[%s]" % (blank(max_score,len(str(w_scores[team][2]))-3),w_scores[team][2]))
      w.write("\n")

  if w:
    w.close()
