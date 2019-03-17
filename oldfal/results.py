# -*- coding: utf-8 -*-
# results.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)

# ----------------------------------------------------------------------------
# PARAMETERS
# ----------------------------------------------------------------------------

import funcs
import properties

week = properties.week
start_wildcards = properties.start_wildcards
week_scores = properties.week_scores
week_dropped = properties.week_dropped
week_favorites = properties.week_favorites
fansub_week = properties.fansub_week
license_week = properties.license_week
double_watching = properties.double_watching
ace_cutoff = properties.ace_cutoff
bench_len = properties.bench_len


deln = 65

def ranking_diff(old_rank, new_rank):
  diff = new_rank - old_rank
  if diff == new_rank or diff == 0:
    return "([color=gray]--[/color])"
  if diff < 0:
    return "([color=green]+%i[/color])" % abs(diff)
  else:
    return "([color=red]-%i[/color])" % diff


# ----------------------------------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------------------------------

def main():

  teams, swaps, aces, wildcards, anime, a_scores, t_scores = funcs.load_all_data(week)
  xteams, xswaps, xaces, xwildcards, xanime, xa_scores, xt_scores = funcs.load_all_data(week-1)

  w = funcs.open_out_file(week, "results")

  # check for name changes
  name_changes = funcs.map_users()
  inv_name_changes = {new[-1]: [initial]+new[:-1] for initial, new in name_changes.items()}


  # -------------------------------------------------------------------------
  # POINTS CRITERIA
  # -------------------------------------------------------------------------

  w.write("Big thanks to ___ for helping out this week.\n\n")
  # TODO: generate this dynamically
  w.write("You can find more details and an overview of all the results in the club's [url=https://myanimelist.net/forum/?topicid=1744449]official FAL Spring 2017 thread[/url].\n\n")
  w.write("[b][u]Points Criteria[/u][/b]\n")
  w.write("Please see the [url=https://myanimelist.net/forum/?topicid=1742552]Rules thread[/url].\n\n")

  # -------------------------------------------------------------------------
  # DISCUSSION POST NOTICE
  # -------------------------------------------------------------------------
  w.write("[b]%s[/b]\n" % ("-"*deln))
  if week % 2 == 0:
    w.write("[b]Discussion posts ARE counted this week[/b]\n")
  else:
    w.write("[b]Discussion posts ARE NOT counted this week[/b]\n")
  w.write("[b]%s[/b]\n\n" % ("-"*deln))

  # -------------------------------------------------------------------------
  # ANIME POINTS
  # -------------------------------------------------------------------------
  w.write("[u]Week %i Anime Points:[/u][spoiler]\n" % week)
  for a_id, info in sorted(anime.items(), key=lambda x:x[1][0].lower()):
    title, (all_posts, posts), count, details, (all_threads, threads), (fansubs, f_score), l_score = info
    watching, completed, dropped, score, favorites = details
    w.write("[u]%s[/u]\n" % title)

    # discussion posts points
    if week % 2 == 0:
      w.write("Episode discussion posts (%i): %i\n" % (posts, posts*25))

    # weekly points
    w.write("Users watching: %i\n" % watching)
    if completed > 0:
      w.write("Users completed: %i\n" % completed)
    if count <= double_watching:
      w.write("In %i or fewer active teams: watching points x2\n" % double_watching)
    if completed > 0 and count <= double_watching:
      w.write("In %i or fewer active teams: completed points x2\n" % double_watching)

    # additional points
    if week in week_scores:
      w.write("Score (%.2f): %i\n" % (score, int(round(score * week_scores[week]))))
    if week in week_dropped:
      w.write("Users dropped (%i): %i\n" % (dropped, dropped*(-1)*week_dropped[week]))
    if week in week_favorites:
      w.write("Favorites (%i): %i\n" % (favorites, favorites*week_favorites[week]))

    # simulcast points
    if week in fansub_week:
      w.write("Simulcast points: %i\n" % f_score)

    # license points
    if week == license_week:
      w.write("License points: %i\n" % (l_score * 10000))
    w.write("Total points: %i\n" % a_scores[a_id][1])
    if title != sorted(anime.values(),key=lambda x:x[0].lower())[-1][0]:
      w.write("\n")
  w.write("[/spoiler]\n\n")

  # -------------------------------------------------------------------------
  # POINTS RANKINGS
  # -------------------------------------------------------------------------
  w.write("[u]Total Weekly Points Rankings:[/u][spoiler]\n")
  for a_id, scores in sorted(a_scores.items(), key=lambda x:x[1][1], reverse=True):
    w.write("%s - %i\n" % (anime[a_id][0].replace("_"," "), scores[1]))
  w.write("[/spoiler]\n\n")

  w.write("[u]Total Overall Points Rankings:[/u][spoiler]\n")
  for a_id, scores in sorted(a_scores.items(), key=lambda x:x[1][0], reverse=True):
    w.write("%s - %i\n" % (anime[a_id][0].replace("_"," "), scores[0]))
  w.write("[/spoiler]\n\n")

  # -------------------------------------------------------------------------
  # HIGHEST UNIQUE SCORE
  # -------------------------------------------------------------------------
  w.write("[u]Highest Unique Team Score:[/u][spoiler]\n")
  w.write("%s\n" % sorted(t_scores.items(), key=lambda x:x[1][3], reverse=True)[0][0])
  w.write("[/spoiler]\n\n")


  # -------------------------------------------------------------------------
  # ACE USERS
  # -------------------------------------------------------------------------
  w.write("[u]Ace users:[/u]\n[spoiler]\n")
  used_aces = 0
  for team, ace_list in sorted(aces.items(), key=lambda x:x[0].lower()):
    old_names = funcs.get_old_names(team, inv_name_changes)
    old_aces = xaces[team]
    new_aces = aces[team]
    print "results"
    print " %s" % team
    print aces[team]
    print "\n"
    if len(old_aces) == len(new_aces):
      continue
    used_aces += 1
    ace = new_aces[-1]
    team_anime = [a[0] for a in teams[team][:-bench_len] if (anime[a[0]][3][0]+anime[a[0]][3][1]) <= ace_cutoff]
    ace_points = [a_scores[a_id][1] for a_id in team_anime]
    if ace not in team_anime or ace_points[team_anime.index(ace)] != max(ace_points):
      w.write("%s - [color=red]%s[/color]\n" % (team, anime[new_aces[-1]][0].replace("_"," ")))
    elif ace_points[team_anime.index(ace)] == max(ace_points):
      w.write("%s - [color=green]%s[/color]\n" % (team, anime[new_aces[-1]][0].replace("_"," ")))
  if used_aces == 0:
    w.write("None\n")
  w.write("[/spoiler]\n\n")

  # -------------------------------------------------------------------------
  # WILDCARD USAGE
  # -------------------------------------------------------------------------
  if week >= start_wildcards:
    wc_booster = []
    wc_nuke_rec = []
    wc_nuke_recoil_rec = []
    wc_extra_swap = []
    for team, wildcard in sorted(wildcards.items(), key=lambda x:x[0].lower()):
      old_names = funcs.get_old_names(team, inv_name_changes)
      if xwildcards[team] != "":
        continue
      if wildcard[5:] == "booster":
        wc_booster.append(team)
      if "nuke-up" in wildcard:
        wc_nuke_rec.append(wildcard[13:])
        wc_nuke_recoil_rec.append(team)
      if "nuke-down" in wildcard:
        wc_nuke_rec.append(wildcard[15:])
        wc_nuke_recoil_rec.append(team)
      if wildcard[5:] == "extra-swap":
        wc_extra_swap.append(team)
    w.write("[u]Wildcard usage:[/u]\n[spoiler]\n")
    w.write("[u]Booster users (+3000 points):[/u]\n")
    if len(wc_booster) == 0:
      w.write("None\n")
    for team in wc_booster:
      w.write("%s%s\n" % (team, old_names))
    w.write("\n[u]Nuke receivers (-6750 points):[/u]\n")
    if len(wc_nuke_rec) == 0:
      w.write("None\n")
    for team in wc_nuke_rec:
      w.write("%s%s\n" % (team, old_names))
    w.write("\n[u]Nuke recoil receivers (-1500 points):[/u]\n")
    if len(wc_nuke_recoil_rec) == 0:
      w.write("None\n")
    for team in wc_nuke_recoil_rec:
      w.write("%s%s\n" % (team, old_names))
    w.write("\n[u]Extra swap users (-1500 points):[/u]\n")
    if len(wc_extra_swap) == 0:
      w.write("None\n")
    for team in wc_extra_swap:
      w.write("%s%s\n" % (team, old_names))
    w.write("[/spoiler]\n\n")

  # -------------------------------------------------------------------------
  # TEAM RANKINGS
  # -------------------------------------------------------------------------
  w.write("[u]Team Rankings:[/u]\n[spoiler]\n")
  ranked_teams = {}
  _, _, _, _, _, _, xt_scores = funcs.load_all_data(week-1)
  for team, info in sorted(t_scores.items(), key=lambda x:x[1][2]):
    ranked_teams.setdefault(info[2], []).append(team)
  for rank, team_list in sorted(ranked_teams.items()):
    for team in sorted(team_list, key=str.lower):
      old_names = funcs.get_old_names(team, inv_name_changes)
      w.write("[b]%i[/b] %s %s%s - %i\n" % (rank, ranking_diff(xt_scores[team][2],rank),\
                                            team, old_names, t_scores[team][0]))
  w.write("[/spoiler]\n\n")

  # -------------------------------------------------------------------------
  # ERROR LOG
  # -------------------------------------------------------------------------
  w.write("[u]Errors:[/u]\n[spoiler]\n")
  e = open("results/week_%.2i_errors.txt" % week).readlines()
  if not e:
    w.write("None\n")
  errors = {}
  for line in e:
    team, error = line.split(" - ")
    errors.setdefault(team, []).append(error.strip())
  for team, error_list in sorted(errors.items()):
    for error in error_list:
      w.write("%s - %s\n" % (team, error))
  w.write("[/spoiler]\n\n")

  if w:
    w.close()
