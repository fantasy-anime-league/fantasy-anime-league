# -*- coding: utf-8 -*-
# ranking_overview.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)

# ----------------------------------------------------------------------------
# PARAMETERS
# ----------------------------------------------------------------------------

import funcs
import properties

week_start = 1
week_end = properties.week
p_num = properties.p_num

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

# formats ranking output
def format_ranking(ranks):
  rank_output = ""
  for i in range(1,len(ranks)):
    rank_output += "%s%i" % (blank(p_num,len(str(ranks[i]))), ranks[i])
    diff = ranks[i] - ranks[i-1]
    if diff == ranks[i] or diff == 0:
      rank_output += "%s(--)  " % (blank(p_num,1))
    elif diff < 0:
      rank_output += "%s(+%i)  " % (blank(p_num,len(str(diff))-1),abs(diff))
    else:
      rank_output += "%s(-%i)  " % (blank(p_num,len(str(diff))), diff)
  return rank_output[:-1]

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

  w = funcs.open_out_file(week_end, "ranking")

  w.write("Ranking Overview; Week %i-%i:\n\n" % (week_start, week_end))

  all_ranks = {}
  for week in range(week_start, week_end+1):
    teams, swaps, aces, wildcards, anime, a_scores, t_scores = funcs.load_all_data(week)

    # get all previous ranks
    for team, (_, _, rank) in t_scores.items():
      all_ranks.setdefault(team, []).append(rank)

  # get length of longest username
  max_name = max([len(team) for team in all_ranks])

  w.write("%s" % blank(max_name,1))
  for week in range(week_start, week_end+1):
    if week < 10:
      w.write("%sweek %i  " % (blank((p_num+p_num),3), week))
    else:
      w.write("%sweek %i  " % (blank((p_num+p_num),4), week))
  w.write("\n")

  for team, ranks in sorted(all_ranks.items(), key=lambda x:x[0].lower()):

    ranking = format_ranking([0]+ranks)
    w.write("%s%s%s\n" % (team, blank(max_name,len(team)-2), ranking))

  if w:
    w.close()
