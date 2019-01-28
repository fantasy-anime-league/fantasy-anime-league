# -*- coding: utf-8 -*-
# details.py
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


# ----------------------------------------------------------------------------
# HELP FUNCTIONS
# ----------------------------------------------------------------------------

# returns a specific number of "whitespaces"
def blank(m, n):
  if m == n:
    return ""
  else:
    return " "*(m-n)

# determines sign
def get_sign(n):
  if n >= 0:
    return "+"
  else:
    return "-"


# ----------------------------------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------------------------------

def main():

  teams, swaps, aces, wildcards, anime, a_scores, t_scores = funcs.load_all_data(week)
  xteams, xswaps, xaces, xwildcards, xanime, xa_scores, xt_scores = funcs.load_all_data(week-1)

  w = funcs.open_out_file(week, "details")

  # check for name changes
  name_changes = funcs.map_users()
  inv_name_changes = {new[-1]: [initial]+new[:-1] for initial, new in name_changes.items()}


  # get all nuke receivers (only if this is the first time of wildcard)
  ### useless?? not used in rest of the code apparently
  nukes = [(t, wc[13:]) for t, wc in wildcards.items() if "nuke-up" in wc and xwildcards[t] == ""]
  nukes.extend([(t, wc[15:]) for t, wc in wildcards.items() if "nuke-down" in wc and xwildcards[t] == ""])


  # get all nuke senders (only if this is the first time the wildcard is used)
  nuke_senders = {t: (wc[5:12], wc[13:]) for t, wc in wildcards.items() if "nuke-up" in wc and xwildcards[t] == ""}
  nuke_senders.update({t: (wc[5:14], wc[15:]) for t, wc in wildcards.items() if "nuke-down" in wc and xwildcards[t] == ""})

  # get all nuke receivers (only if this is the first time the wildcard is used)
  nuke_recs = {}
  for sender, (nuke, rec) in nuke_senders.items():
    nuke_recs.setdefault(rec, []).append((nuke, sender))

  # -------------------------------------------------------------------------
  # STATUS
  # -------------------------------------------------------------------------
  for team in sorted(teams, key=str.lower):
    old_names = funcs.get_old_names(team, inv_name_changes)
    #w.write("%s\n| %s%s |\n%s\n" % (("-"*(len(team+old_names)+4)), team, old_names, ("-"*(len(team+old_names)+4))))
    tmp_str = "Team: %s%s" % (team, old_names)
    #w.write("%s\n%s\n\n" % (tmp_str, ("-"*len(tmp_str))))
    w.write("%s\n\n" % (tmp_str))
    tmp_str = "Status before week %i:" % week
    w.write("%s\n%s\n" % (tmp_str, ("-"*len(tmp_str))))
    w.write("Rank: %i\n" % xt_scores[team][2])
    w.write("All points: %i\n" % xt_scores[team][0])
    if team != 'Squirrel500' and team != 'starlightshine':
      w.write("Active team: %s\n" % ", ".join(sorted([t[1] for t in xteams[team][:-2]])))
      w.write("Bench: %s\n" % ", ".join(sorted([t[1] for t in xteams[team][-2:]])))
    w.write("Swaps left: %i\n\n" % xswaps[team][0])

    # -------------------------------------------------------------------------
    # SWAPS
    # -------------------------------------------------------------------------
    w.write("Swaps:\n")
    if xteams[team][-1][1] != teams[team][-1][1]:
      w.write("out: %s\nin:  %s\n\n" % (teams[team][-1][1], xteams[team][-1][1]))
    elif xteams[team][-2][1] != teams[team][-2][1]:
      w.write("out: %s\nin:  %s\n\n" % (teams[team][-2][1], xteams[team][-2][1]))
    else:
      w.write("None\n\n")

    # -------------------------------------------------------------------------
    # UNIQUE TEAM SCORE
    # -------------------------------------------------------------------------
    w.write("Unique Team Score:\n")
    if t_scores[team][3] != week:
      w.write("None\n\n")
      upoints = 0
    else:
      w.write("%i\n\n" % 4000)
      upoints = 4000

    # -------------------------------------------------------------------------
    # ACES
    # -------------------------------------------------------------------------
    w.write("Ace:\n")
    a_points = 0
    old_aces = xaces[team]
    new_aces = aces[team]
    print "%s \n" % team
    print xaces[team]
    print "\n"
    print aces[team]
    print "\n"
    if len(old_aces) == len(new_aces):
      w.write("None\n\n")
    else:
      ace = new_aces[-1]
      team_anime = [a[0] for a in teams[team][:-2] if (anime[a[0]][3][0]+anime[a[0]][3][1]) <= ace_cutoff]
      ace_points = [a_scores[a_id][1] for a_id in team_anime]
      if ace not in team_anime or ace_points[team_anime.index(ace)] != max(ace_points):
        w.write("%s: %i\n" % (anime[new_aces[-1]][0], -3000))
        a_points = -3000
      elif ace_points[team_anime.index(ace)] == max(ace_points):
        w.write("%s: %i\n" % (anime[new_aces[-1]][0], 3000))
        a_points = 3000
      w.write("\n")
      #w.write("=> %i\n\n" % a_points)

    # -------------------------------------------------------------------------
    # WILDCARDS
    # -------------------------------------------------------------------------
    w.write("Wildcards:\n")
    w_points = 0

    if week < start_wildcards:
      w.write("Not yet available\n\n")
    else:
      if (wildcards[team] == "" or xwildcards[team] != "") and team not in nuke_recs:
        w.write("None\n")
      if wildcards[team] != "" and xwildcards[team] == "":
        wildcard = wildcards[team][5:]
        if wildcard == "booster":
          w.write("%s: %i\n" % (wildcard.capitalize(), 3000))
          w_points += 3000
        elif wildcard == "extra-swap":
          w.write("%s: %i\n" % (wildcard.capitalize(), -1500))
          w_points -= 1500
        else:
          w.write("%s sent to %s: %i\n" % (nuke_senders[team][0].capitalize(), nuke_senders[team][1], -1500))
          w_points -= 1500
      if team in nuke_recs:
        for nuke, sender in sorted(nuke_recs[team], key=lambda x:x[1].lower()):
          w.write("%s received from %s: %i\n" % (nuke.capitalize(), sender, -6750))
          w_points -= 6750
      w.write("\n")
      #w.write("=> %i\n\n" % w_points)

    # -------------------------------------------------------------------------
    # WEEKLY POINTS: WATCHING/COMPLETED
    # -------------------------------------------------------------------------
    tmp_str = "Week %i watching points:" % week
    w.write("%s\n%s\n" % (tmp_str, ("-"*len(tmp_str))))
    weekly_points = 0
    if team != 'starlightshine':
      for a_id, a_title in sorted(teams[team][:-2], key=lambda x:x[1]):
        watching, completed, _, _, _ = anime[a_id][3]
        w.write("%s\n" % anime[a_id][0])
        w.write("- Watching: %i\n" % watching)
        weekly_points += watching
        if completed > 0:
          w.write("- Completed: %i\n" % completed)
          weekly_points += completed
        if anime[a_id][2] <= double_watching:
          w.write("- Watching x2: %i\n" % watching)
          weekly_points += watching
        if completed > 0 and anime[a_id][2] <= double_watching:
          w.write("- Completed x2: %i\n" % completed)
          weekly_points += completed

    w.write("=> %i\n\n" % weekly_points)

    # -------------------------------------------------------------------------
    # FORUM POSTS
    # -------------------------------------------------------------------------
    tmp_str = "Week %i discussion post points:" % week
    w.write("%s\n%s\n" % (tmp_str, ("-"*len(tmp_str))))
    forum_points = 0
    if week % 2 == 1:
      w.write("Discussion posts ARE NOT counted this week\n\n")
    else:
      if team != 'starlightshine':
        for a_id, a_title in sorted(teams[team][:-2], key=lambda x:x[1]):
          w.write("%s (%i): %i \n" % (anime[a_id][0], anime[a_id][1][1], anime[a_id][1][1]*25))
          forum_points += anime[a_id][1][1]*25
        w.write("=> %i\n\n" % forum_points)

    # -------------------------------------------------------------------------
    # SPECIAL WEEK POINTS
    # -------------------------------------------------------------------------
    addpoints = 0
    if week in week_scores or week in week_dropped or week in week_favorites:
      tmp_str = "Week %i additional points:" % week
      w.write("%s\n%s\n" % (tmp_str, ("-"*len(tmp_str))))
      if team != 'starlightshine':
        for a_id, a_title in sorted(teams[team][:-2], key=lambda x:x[1]):
          scorepoints = 0
          w.write("%s\n" % anime[a_id][0])
          _, _, dropped, score, favs = anime[a_id][3]
          if week in week_scores:
            w.write("- Score (%.2f): %i\n" % (score, int(round(score * week_scores[week]))))
            scorepoints += int(round(score * week_scores[week]))
          if week in week_dropped:
            w.write("- Dropped (%i): %i\n" % (dropped, dropped*(-1)* week_dropped[week]))
            scorepoints += dropped * (-1)* week_dropped[week]
          if week in week_favorites:
            w.write("- Favorites (%i): %i\n" % (favs, favs*week_favorites[week]))
            scorepoints += favs * week_favorites[week]
          addpoints += scorepoints
        w.write("=> %i\n\n" % addpoints)

    # -------------------------------------------------------------------------
    # SIMULCAST POINTS
    # -------------------------------------------------------------------------
    if week in fansub_week:
      tmp_str = "Week %i simulcast points:" % week
      w.write("%s\n%s\n" % (tmp_str, ("-"*len(tmp_str))))
      fansub_points = 0
      if team != 'starlightshine':
        for a_id, a_title in sorted(teams[team][:-2], key=lambda x:x[1]):
          w.write("%s: %i \n" % (anime[a_id][0], anime[a_id][5][1]))
          fansub_points += anime[a_id][5][1]
        w.write("=> %i\n\n" % fansub_points)
        addpoints += fansub_points

    # -------------------------------------------------------------------------
    # LICENSE POINTS
    # -------------------------------------------------------------------------
    if week == license_week:
      tmp_str = "Week %i license points:" % license_week
      w.write("%s\n%s\n" % (tmp_str, ("-"*len(tmp_str))))
      license_points = 0
      for a_id, a_title in sorted(teams[team][:-2], key=lambda x:x[1]):
        if anime[a_id][6] == 1:
          w.write("%s: %i \n" % (anime[a_id][0], 10000))
        license_points += anime[a_id][6] * 10000
      w.write("=> %i\n\n" % license_points)
      addpoints += license_points

    # -------------------------------------------------------------------------
    # SUM UP POINTS
    # -------------------------------------------------------------------------
    addxpoints = addpoints + upoints
    w.write("\nwildcards    ace    watching    posts    additional\n")
    if get_sign(w_points) == "+":
      sign = ""
    else:
      sign = "-"
    w.write("%s%s%i" % (sign, blank(len("wildcards"),(len(str(abs(w_points)))+len(sign))), abs(w_points)))
    w.write(" %s%s %i" % (get_sign(a_points), blank(len(" ace"),len(str(abs(a_points)))), abs(a_points)))
    w.write("  +%s %i" % (blank(len("watching"),len(str(weekly_points))), weekly_points))
    w.write("  +%s %i" % (blank(len("posts"),len(str(forum_points))), forum_points))
    w.write("  %s%s %i" % (get_sign(addxpoints),blank(len("additional"),len(str(abs(addxpoints)))), abs(addxpoints)))
    w.write("\n\n\n")

    # -------------------------------------------------------------------------
    # STATUS
    # -------------------------------------------------------------------------
    tmp_str = "Status after week %i:" % week
    w.write("%s\n%s\n" % (tmp_str, ("-"*len(tmp_str))))
    w.write("Rank: %i\n" % t_scores[team][2])
    w.write("New points: %i\n" % t_scores[team][1])
    w.write("All points: %i\n" % t_scores[team][0])
    if team != 'Squirrel500' and team != 'starlightshine':
      w.write("Active team: %s\n" % ", ".join(sorted([t[1] for t in teams[team][:-2]])))
    if team != 'Squirrel500' and team != 'starlightshine':  
      w.write("Bench: %s\n" % ", ".join(sorted([t[1] for t in teams[team][-2:]])))
    w.write("Swaps left: %i\n" % swaps[team][0])
    next_swap = swaps[team][1]
    if next_swap == 0:
      w.write("Next swap available: in week %i\n" % (week+1))
    else:
      w.write("Next swap available: in week %i\n" % (week+next_swap))
    #w.write("\n%s\n\n" % ("-"*104))
    w.write("\n%s\n\n" % ("#"*60))
  if w:
    w.close()
