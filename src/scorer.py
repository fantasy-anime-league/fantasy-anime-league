# -*- coding: utf-8 -*-
# scorer.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)

# ----------------------------------------------------------------------------
# PARAMETERS
# ----------------------------------------------------------------------------

import funcs
import properties

import httplib
import urllib
import random
import re
import time

import gzip
import StringIO

import pickle

#from bs4 import BeautifulSoup

week = properties.week
post_start = properties.post_start
post_end = properties.post_end
page_start = properties.page_start
page_end = properties.page_end
start_wildcards = properties.start_wildcards
week_scores = properties.week_scores
week_dropped = properties.week_dropped
week_favorites = properties.week_favorites
fansub_week = properties.fansub_week
license_week = properties.license_week
double_watching = properties.double_watching
ace_cutoff = properties.ace_cutoff
a_thread = properties.a_thread
bench_len = properties.bench_len
swap_number = properties.swap_number
swap_delay = properties.swap_delay
delay = properties.delay

# ----------------------------------------------------------------------------
# HELP FUNCTIONS
# ----------------------------------------------------------------------------

# removes commas from numbers
def get_int(string):
	return int(string.replace(",",""))

# if a series was renamed AFTER FAL started, correct it here from old title to new title
def correct_title(title):
	if title == "Break Blade":
		return "Break Blade (TV)"
	if title == "KutsuDaru.":
		return "Kutsushita ga Daru Daru ni Nacchau Wake: Imadoki Youkai Zukan"
	if title == "Ryuugajou Nanana no Maizoukin (TV)":
		return "Ryuugajou Nanana no Maizoukin"
	if title == "Mangaka-san to Assistant-san to The Animation":
		return "Mangaka-san to Assistant-san to"
	if title == "Abarenbou Rikishi!! Matsutarou":
		return "Abarenbou Kishi!! Matsutarou"
	if title == "High School Star Musical":
		return "Starmyu"
	if title == "Room Mate":
		return "Room Mate: One Room Side M"
	if title == "Amai Choupatsu: Watashi wa Kanshuu Senyou Pet":
		return "Amai Choubatsu: Watashi wa Kanshu Senyou Pet"
	if title == "Lupin III: Part V":
		return "Lupin III: Part 5"

	return title


# ----------------------------------------------------------------------------
# MAL SERVER FUNCTIONS
# ----------------------------------------------------------------------------

def process_stats(a_id, a_title, httpconn):
	"""
	Retrieves numbers from the stats page of an anime.

	@param a_id anime ID
	@param a_title anime title
	@param httpconn HTTPConnection object

	@return tuple of watching, completed, dropped, score, favorites
	"""

	if a_title.endswith("?"):
		a_title = a_title.strip("?")
		print a_title
		a_title = "Shuumatsu Nani Shitemasu ka Isogashii desu ka Sukutte Moratte Ii desu ka"

	time.sleep(delay)
	params, headers = funcs.header()
	
	print a_title
	httpconn.connect()
	#experienced issues with ID for Flying Witch. Using a hard override for now.
	if (a_id == "46258"):
		a_id = 31376
	print a_id
	print a_title

	if a_id == "33094":
		httpconn.request("GET", "/anime/%s/%s/stats" % (a_id, "WWWWorking"), params, headers)
	elif a_id == "32038":
		httpconn.request("GET", "/anime/%s/%s/stats" % (a_id, "Show_By_Rock_"), params, headers)
	else:
		httpconn.request("GET", "/anime/%s/%s/stats" % (a_id, a_title.replace(" ","_")), params, headers)
	
	res = httpconn.getresponse()
	if res.getheader("Content-Encoding") == "gzip":
		response = gzip.GzipFile(fileobj = StringIO.StringIO(res.read())).read()
	else:
		response = res.read()
	httpconn.close()
	watching = get_int(re.search('Watching:</span> ([\d,]+)', response).group(1))

	#for manually inputting values
	"""
	if (a_id == "32601"):# 12-sai.: Chicchana Mune no Tokimeki
		watching = 2987
	elif (a_id == "31080"):# Anne Happy♪
		watching = 7883
	elif (a_id == "30795"):# Bakuon!!
		watching = 8725
	elif (a_id == "31904"):# Big Order (TV)
		watching = 0
	elif (a_id == "31733"):# Bishoujo Senshi Sailor Moon Crystal Season III
		watching = 4400
	elif (a_id == "32313"):# Concrete Revolutio: Choujin Gensou - The Last Song
		watching = 3775
	elif (a_id == "32608"):# Endride
		watching = 13161
	elif (a_id == "31376"):# Flying Witch
		watching = 13132
	elif (a_id == "31630"):# Gyakuten Saiban: Sono "Shinjitsu", Igi Ari!
		watching = 26313
	elif (a_id == "31500"):# Haifuri
		watching = 5230
	elif (a_id == "31338"):# Hundred 
		watching = 18873
	elif (a_id == "31933"):# JoJo no Kimyou na Bouken: Diamond wa Kudakenai
		watching = 21089
	elif (a_id == "31405"):# Joker Game
		watching = 29766
	elif (a_id == "32682"):# Kagewani: Shou
		watching = 3785
	elif (a_id == "31798"):# Kiznaiver
		watching = 29760
	elif (a_id == "31804"):# Kuma Miko 
		watching = 13744
	elif (a_id == "32245"):# Kuromukuro 
		watching = 5865
	elif (a_id == "31610"):# Kyoukai no Rinne (TV) 2nd Season
		watching = 2598
	elif (a_id == "28013"):# Macross Δ
		watching = 6214
	elif (a_id == "31741"):# Magi: Sinbad no Bouken (TV) 
		watching = 0
	elif (a_id == "32438"):# Mayoiga
		watching = 39467
	elif (a_id == "32792"):# Mobile Suit Gundam Unicorn RE:0096
		watching = 3126
	elif (a_id == "31404"):# Netoge no Yome wa Onnanoko ja Nai to Omotta?
		watching = 23482
	elif (a_id == "32606"):# Onigiri
		watching = 3963 
	elif (a_id == "31498"):# Pan de Peace!
		watching = 7798
	elif (a_id == "31240"):# Re:Zero kara Hajimeru Isekai Seikatsu
		watching = 37830
	elif (a_id == "32542"):# Sakamoto desu ga? 
		watching = 29997
	elif (a_id == "31564"):# Sansha Sanyou
		watching = 1519
	elif (a_id == "32595"):# Seisen Cerberus: Ryuukoku no Fatalités
		watching = 15291
	elif (a_id == "32175"):# Shounen Maid
		watching = 5912
	elif (a_id == "32105"):# Sousei no Onmyouji
		watching = 27479
	elif (a_id == "31680"):# Super Lovers
		watching = 7857
	elif (a_id == "32093"):# Tanaka-kun wa Itsumo Kedaruge 
		watching = 10331
	elif (a_id == "31430"):# Terra Formars Revenge
		watching = 9720
	elif (a_id == "32681"):# Uchuu Patrol Luluco
		watching = 13236
	elif (a_id == "31098"):# Ushio to Tora (TV) 2nd Season
		watching = 11205
	elif (a_id == "31439"):# Wagamama High Spec
		watching = 0
	"""

	completed = get_int(re.search('Completed:</span> ([\d,]+)', response).group(1))
	print completed
	dropped = get_int(re.search('Dropped:</span> ([\d,]+)', response).group(1))
	score = re.search('>Score:</span>\n\s*<span(?: itemprop="ratingValue")?>([^<]+)</span>', response).group(1)
	if "N/A" not in score:
		score = float(score)
	else:
		score = 0.0
	favorites = get_int(re.search('Favorites:</span>\n\s*([\d,]+)', response).group(1))
	status = re.search('>Status:</span>\n\s*(.+?)\n\s*</div>', response).group(1)
	date = re.search('>Aired:</span>\n\s*(.+?)\n\s*</div>', response).group(1)
	# set everything that people cannot do legitimately to zero
	# (there are workarounds to set an anime to completed even though it's still airing, this does NOT count for FAL.
	#  since the cron that is responsible for moving wrongly set entries back runs only once a day, we correct this in the script.)
	if "Currently" in status:
		completed = 0
		# prints all currently airing series to check if one needs to be set to completed
		# (usually the cron on the MAL server does this 1 day earlier but it can happen that it stops working)
		print "%s (currently) - %s" % (date, a_title)
	if "Not yet aired" in status:
		watching = 0
		completed = 0
		dropped = 0
		# prints all not yet aired series to check if one needs to be set to aired
		# (usually the cron on the MAL server does this 1 day earlier but it can happen that it stops working)
		print "%s (not yet aired) - %s" % (date, a_title)

	return (watching, completed, dropped, score, favorites)


def process_posts(a_id, a_title, show, posts, threads, httpconn):
	"""
	Retrieves number of forum posts made for episode discussions.

	@param a_id anime ID
	@param show page identification for sub-forums. show=0 first page, +50 for every next page
	@param posts sum of all posts in episode discussion threads (ignore other threads)
	@param httpconn HTTPConnection object

	@return sum of all existing discussion posts for this anime ID
	"""
	print("process_posts")

	time.sleep(delay)
	params, headers = funcs.header()
	httpconn.connect()
	httpconn.request("GET", "/forum/?animeid=%s&show=%i" % (a_id, show), params, headers)
	res = httpconn.getresponse()
	if res.getheader("Content-Encoding") == "gzip":
		response = gzip.GzipFile(fileobj = StringIO.StringIO(res.read())).read()
	else:
		response = res.read()
	httpconn.close()

	pages = int(re.search('Pages \((\d+)\)', response).groups(1)[0])
	# no single thread exists in the subboard
	if pages == 0:
		return (0, 0)
	# get the current title of the episode threads (x_title)
	t_pattern = 'forum_locheader">(.+?)</h1>'
	a_title = re.search(t_pattern, response).groups(1)[0]
	x_title = re.escape(a_title)
	x_title = x_title.replace("&","&amp;")
	# count posts: sum of all replies and number of threads (len of found threads)
	# (the replies column doesn't include the first post! needs to be counted extra (number of threads))
	posts += sum([get_int(z) for z in re.findall('%s Episode \d+ Disc.+?boardrow.+?>([\d,]+)<' % x_title, response, re.S)]) # replies
	posts += len(re.findall('%s Episode \d+ Disc.+?boardrow.+?>([\d,]+)<'% x_title, response, re.S)) # number of topics
	# count threads: len of found threads
	threads += len(re.findall('%s Episode \d+ Disc.+?boardrow.+?>([\d,]+)<'% x_title, response, re.S))

	# this is to check the number of threads. this is important because if an entry gets renamed, new threads will have
	# the new title while old threads still have the old title and then the RegEx misses threads/posts
	# [X] = this is the number of found threads
	# after [X] is a list of found episode discussion threads
	# for example [2] 5, 4 -- this means only 2 threads were found (ep 4, 5) and 1-3 were not found
	# if this happens please ask a Forum Mod or DB Admin to rename the OLD threads so the title matches again
	print "%s" % a_title
	all_eps = sorted(re.findall('%s Episode (\d+) Disc.+?boardrow.+?>[\d,]+<' % x_title, response, re.S),reverse=True)
	print "[%i] %s\n" % (len(all_eps), " ".join([str(z) for z in all_eps]))

	if show/50+1 == pages:
		return (posts, threads)
	else:
		return process_posts(a_id, a_title, show+50, posts, threads, httpconn)


def get_swaps(page, actions, httpconn):
	"""
	Collects swaps for the current week.

	This function accesses the swap thread.

	@param page page identification for threads
	@param actions list of tuples (username, post content)
	@param httpconn HTTPConnection object

	@return list of tuples (username, post content = swap)
	"""
	print("get_swaps")

	time.sleep(delay)
	params, headers = funcs.header()
	print httpconn
	httpconn.connect()
	httpconn.request("GET", "/forum/?topicid=%s&show=%i" % (a_thread, (page-1)*50), params, headers)
	res = httpconn.getresponse()
	if res.getheader("Content-Encoding") == "gzip":
		response = gzip.GzipFile(fileobj = StringIO.StringIO(res.read())).read()
	else:
		response = res.read()
	httpconn.close()
	pattern = 'postnum">(\d+).+?row2.+?<strong>(.+?)</strong>.+?row1.+?message\d.+?class="clearfix">(.+?)</div>'
	actions.extend(re.findall(pattern, response, re.S))
	if page == page_end:
		return [tuple(a[1:]) for a in actions\
						if int(a[0]) >= post_start and int(a[0]) <= post_end]
	else:
		return get_swaps(page+1, actions, httpconn)


# ----------------------------------------------------------------------------
# OTHER DATA FUNCTIONS
# ----------------------------------------------------------------------------

def get_wildcards(wildcards, e):
	"""
	Gets wildcards from a text file.

	Checks for the following errors:
	- Team does not exist (not registered or user has renamed himself)
	- Only first wildcard was used (user requested more than one in this week)
	- Wildcard already used (in a week before)
	- Wildcards not yet available

	@param wildcards wildcards dictionary from last week
	@param e writer for errors

	@return wildcards dictionary with new (unused) wildcards
	"""
	print("get_wildcards")
	print wildcards

	wc_users = []
	for line in open("wildcards.txt").readlines():
		team = line.split()[0]
		wildcard = " ".join(line.split()[1:])
		if team not in wildcards:
			e.write("%s - invalid team (wildcard request)\n" % team)
		elif team in wc_users:
			e.write("%s - only first wildcard was used\n" % team)
		elif wildcards[team] != "":
			e.write("%s - wildcard already used\n" % team)
		elif week < start_wildcards:
			e.write("%s - wildcards not yet available\n" % team)
		else:
			wildcards[team] = wildcard.strip()
			wc_users.append(team)
	return wildcards


def get_aces(aces, teams, anime, mapping, e):
	"""
	Gets aces from a text file.

	Checks for the following errors:
	- Team does not exist (not registered or user has renamed himself)
	- Only first valid ace was used (user requested more than one in this week)
	- Ace already used (in a week before)
	- Ace not in active team (but it's an eligible title)
	- Invalid ace request (e.g., spelling errors)
	- Ace no longer eligible (Xk+ watching+completed)

	@param aces aces dictionary from last week
	@param teams teams dictionary from last week
	@param mapping {a_title:a_id} mapping

	@return tuple of aces dictionary (with the new aces) and a list of (team, ace) tuples [could be done better]
	"""
	print("get_aces")

	new_aces = []
	for line in open("aces.txt").readlines():
		print "ace:"
		team = line.split()[0]
		ace_title = " ".join(line.split()[1:])



		if ace_title in mapping:
			ace = mapping[ace_title]
			print "%s \n" % team
			#print "%d \n" % anime[ace][3][0]
			#print "%d \n" % anime[ace][3][1]
			if team not in teams:
				e.write("%s - invalid team (ace request)\n" % team)
			elif team in [t[0] for t in new_aces]:
				e.write("%s - only first valid ace was used\n" % team)
			elif ace in aces[team]:
				e.write("%s - ace already used\n" % team)
			elif ace not in [idx for idx, wc in teams[team]]:
				e.write("%s - ace not in active team\n" % team)
			elif (anime[ace][3][0] + anime[ace][3][1]) > ace_cutoff:
				e.write("%s - ace no longer eligible (50k+ watching+completed)\n" % team)
				print "error\n"
			else:
				print "added\n"
				aces[team].append(ace)
				new_aces.append(tuple((team,ace)))
		else:
			e.write("%s - invalid ace request\n" % team)
	return (aces, new_aces)


def get_fansubs(anime, mapping, retrieve):
	"""
	Gets simulcast info from a text file.
	Was the old fansub/simulcast function before. Could be made simpler now that the fansub info is not used anymore.

	@return
	"""
	print "fetching simuls"
	for line in open("fansubs%.2i.txt" % week).readlines():
		print "HELLO"
		a_title = line.split("=")[0].strip()
		subs = line.split("=")[1].split()
		anime[mapping[a_title]][5][0] = subs
		old_score = anime[mapping[a_title]][5][1]
		print old_score
		sub_score = 0
		for entry in subs:
			if entry == "simul":
				sub_score += 2000
		#sub_score -= old_score
		anime[mapping[a_title]][5][1] = sub_score
		print a_title, sub_score
	return anime


def get_licenses(anime, mapping):
	"""
	Gets licenses from a text file.

	@return
	"""
	for line in open("licenses.txt").readlines():
		anime[mapping[line.strip()]][6] = 1

	return anime


# ----------------------------------------------------------------------------
# CALCULATION FUNCTIONS
# ----------------------------------------------------------------------------


def get_score(a_id, a_info, week, httpconn):
	"""
	Calculates the score for a given anime title and week.

	@param a_id anime ID
	@param a_info value of anime dictionary
	@param week the specified week
	@param httpconn HTTPConnection object

	@return tuple of score for all stats, posts, special points; number of new posts since the last week; list of numbers of watching, completed, dropped, anime score, and favorites
	"""

	score = 0 # initialize score
	new_posts = 0 # needs to be declared for odd weeks
	new_threads = 0 # needs to be declared for odd weeks

	# Since World Trigger: Toubousha-hen was removed from the database mid-game,
	# we'll stop tracking points for it
	if a_id == "31316":
		return (0, 0, [0, 0, 0, 0, 0], 0)

	# weekly scores
	watching, completed, dropped, a_score, favorites = process_stats(a_id, a_info[0], httpconn)

	detailed_info = [watching, completed, dropped, a_score, favorites]
	score += watching + completed # add watching/completed
	if a_info[2] <= double_watching: # double watching/completed points if less or equal than X teams
		score += watching + completed
	#count posts only every two weeks
	if week % 2 == 0:
		all_posts, all_threads = process_posts(a_id, a_info[0], 0, 0, 0, httpconn)
		new_posts = all_posts - a_info[1][0] # diff of old and new post count
		new_threads = all_threads - a_info[4][0] # diff of old and new thread count

		### posts before FAL started get subtracted (INCLUDING thread numbers), e.g. Diabolik Lover
		if a_id == "37496":
			new_posts -= 42
		elif a_id == "37561":
			new_posts -= 42
		elif a_id == "37430":
			new_posts -= 170
		elif a_id == "37965":
			new_posts -= 14
		elif a_id == "35835":
			new_posts -= 81
		elif a_id == "37991":
			new_posts -= 36

		score += new_posts * 25

	# additional points
	if week in week_scores:
		score += int(round(a_score * week_scores[week]))
	if week in week_dropped:
		score -= dropped * week_dropped[week]
	if week in week_favorites:
		score += favorites * week_favorites[week]

	#for disqualified titles; set everything to 0
	if a_id == '34866':
		return (0, 0, [0,0,0,0,0], 0)

	return (score, new_posts, detailed_info, new_threads)


# ----------------------------------------------------------------------------
# OTHER FUNCTIONS
# ----------------------------------------------------------------------------

def get_ranking(t_scores):
	"""
	Computes team rankings based on the current score.

	If two or more teams share the same rank, they obtain the same rank number. The rank number(s)
	between these teams and the team(s) below are skipped.

	@param t_scores team score dictionary

	@return ranked team dictionary {userA:1,userB:2,userC:2,userD:4,...}
	"""

	r_scores = {}
	prev = None
	for i, (team, scores) in enumerate(sorted(t_scores.items(), key=lambda x:x[1][0], reverse=True)):
		if scores[0] != prev:
			rank = i + 1
			prev = scores[0]
		r_scores[team] = rank
	return r_scores


# this function needs to be rewritten so that it's easier to make changes to wildcards in the future
def use_wildcards(wildcards, t_scores, swaps, e):
	"""
	Processes wildcards.

	@param wildcards wildcard dictionary
	@param t_scores team score dictionary (bonus/penalities)
	@param swaps swaps dictionary (change if extra swap)
	@param e writer for errors

	@return tuple of changed (wildcards, t_scores, swaps)
	"""

	wildcards = get_wildcards(wildcards, e)
	if week < start_wildcards:
		return (wildcards, t_scores, swaps)
	else:
		ranking = get_ranking(t_scores) # use ranking from previous week
		inv_ranking = {}
		# inv_ranking = {1:[userA],2:[userB,userC],4:[userD],...}
		for team, rank in ranking.items():
			inv_ranking[rank] = inv_ranking.get(rank, [])
			inv_ranking[rank].append(team)
		for team, wildcard in wildcards.items():
			if wildcard == "" or wildcard.startswith("used"):
				continue
			if wildcard == "booster":
				t_scores[team][1] += 3000
			elif wildcard == "nuke-up":
				my_rank = ranking[team]
				above_rank = inv_ranking[my_rank][:] # get teams of the same rank
				above_rank.remove(team) # but not the team itself
				# team is rank 1 and doesn't share this rank: do nothing
				# but delete wildcard so that the user can use another one
				if my_rank == 1 and not above_rank:
					e.write("%s - no team above you to nuke\n" % team)
					wildcards[team] = ""
					continue
	# only get teams of above rank if it's not rank 1
	# if it's rank 1 use the current above_rank = teams that share rank 1
				if my_rank > 1:
		# get teams of above rank (use actual rank in list)
					next_rank = inv_ranking.keys()[inv_ranking.keys().index(my_rank)-1]
					above_rank.extend(inv_ranking[next_rank])
				t_scores[team][1] -= 1500
				nuke_rec = above_rank[random.randint(0,len(above_rank)-1)]
				t_scores[nuke_rec][1] -= 6750
				wildcard = "%s_%s" % (wildcard, nuke_rec)
			elif wildcard == "nuke-down":
				my_rank = ranking[team]
				below_rank = inv_ranking[my_rank][:] # get teams of the same rank
				below_rank.remove(team) # but not the team itself
				# team is last ranked and doesn't share this rank: do nothing
				# but delete wildcard so that the user can use another one
				if my_rank == sorted(inv_ranking.keys())[-1] and not below_rank:
					e.write("%s - no team below you to nuke\n" % team)
					wildcards[team] = ""
					continue
				# only get teams of below rank if it's not the last rank
				if my_rank < sorted(inv_ranking.keys())[-1]:
					# get teams of below rank (use actual rank in list)
					next_rank = inv_ranking.keys()[inv_ranking.keys().index(my_rank)+1]
					below_rank.extend(inv_ranking[next_rank])
				t_scores[team][1] -= 1500
				nuke_rec = below_rank[random.randint(0,len(below_rank)-1)]
				t_scores[nuke_rec][1] -=6750
				wildcard = "%s_%s" % (wildcard, nuke_rec)
			elif wildcard == "extra-swap":
				t_scores[team][1] -= 1500
				swaps[team][0] += 1
				swaps[team][1] = 0
			wildcards[team] = "used_%s" % wildcard
	return (wildcards, t_scores, swaps)


def make_swaps(teams, bench, swaps, anime, mapping, httpconn, e):
	"""
	Processes swaps collected from the swap thread.

	@param teams team dictionary (without bench!)
	@param bench bench dictionary
	@param swaps swaps dictionary (available swaps and delay)
	@param anime anime dictionary (look for correct titles)
	@param mapping {a_title:a_id} mapping
	@param httpconn HTTPConnection object
	@param e writer for errors

	@return tuple of changed (teams, bench, swaps)
	"""

	for team, info in swaps.items():
		if info[1] > 0:
			swaps[team][1] -= 1 # reduce swap delay

	swap_list = get_swaps(page_start, [], httpconn)
	#swap_list[0] = ('Niveen_Sleem', 'Natsume Yuujinchou Roku<br />\n<br />\nEromanga-sensei')
	print swap_list
	made_swaps = []
	for team, swap in swap_list:
		print "SWAPPING"
		print team
		# hack to remove blank lines
		swx = "/".join(swap.split("<br />")).replace("\n","").replace("//","/")
		sw = "/".join(swx.split("/")[:2])

		if not re.findall('.+?/.+', sw):
			e.write("%s - invalid swap request (wrong format)\n" % team)
			continue
		if team not in teams:
			e.write("%s - invalid team (swap request)\n" % team)
			continue
		if team in made_swaps:
			e.write("%s - only first valid swap was used\n" % team)
			continue
		if swaps[team][0] == 0:
			e.write("%s - no more swaps left\n" % team)
			continue
		if swaps[team][1] > 0:
			e.write("%s - next swap available in week %i\n" % (team, (week+swaps[team][1])))
			continue

		old_title, new_title = re.findall('(.+?)/(.+)', sw)[0]
		old_title = old_title.strip()
		new_title = new_title.strip()

		# fix titles that got renamed
		old_title = correct_title(old_title)
		new_title = correct_title(new_title)

		print old_title
		print new_title

		### FIX Sareta
		if "Sareta" in old_title:
			old_title = "Ore ga Ojousama Gakkou ni \"Shomin Sample\" Toshite Gets♥Sareta Ken"
		if "Sareta" in new_title:
			new_title = "Ore ga Ojousama Gakkou ni \"Shomin Sample\" Toshite Gets♥Sareta Ken"
		### FIX Macross
		if "Macross" in old_title:
			old_title = "Macross Δ"
		if "Macross" in new_title:
			new_title = "Macross Δ"
		### FIX Quotes
		if "Gyakuten" in old_title:
			old_title = "Gyakuten Saiban: Sono \"Shinjitsu\", Igi Ari!"
		if "Gyakuten" in new_title:
			new_title = "Gyakuten Saiban: Sono \"Shinjitsu\", Igi Ari!"

		if "Cerberus" in old_title:
			old_title = "Seisen Cerberus: Ryuukoku no Fatalités"
		if "Cerberus" in new_title:
			new_title = "Seisen Cerberus: Ryuukoku no Fatalités"

		if "Trickster" in old_title:
			old_title = "Trickster: Edogawa Ranpo \"Shounen Tanteidan\" yori"
		if "Trickster" in new_title:
			new_title = "Trickster: Edogawa Ranpo \"Shounen Tanteidan\" yori"

		if "Senkan" in old_title:
			old_title = "Uchuu Senkan Tiramisù"
		if "Senkan" in new_title:
			new_title = "Uchuu Senkan Tiramisù"

		#old_title = BeautifulSoup(old_title).get_text()
		#new_title = BeautifulSoup(new_title).get_text()

		if "Working" in old_title:
			old_title = "WWW.Working!!"
		if "Working" in new_title:
			new_title = "WWW.Working!!"

		if "Prince" in old_title:
			old_title = "Uta no☆Prince-sama♪ Maji Love Legend Star"
		if "Prince" in new_title:
			new_title = "Uta no☆Prince-sama♪ Maji Love Legend Star"

		if team == 'Niveen_Sleem':
			new_title = 'Release the Spyce'

		# at least one title doesn't match the eligible titles
		# try to autocorrect them
		if old_title not in mapping and team != 'LoneWizard' and team != 'Rystlnix':
			tmp_title = funcs.spelling_correction(old_title)
			if tmp_title == "": # no correction possible
				e.write("%s - invalid swap request (active team title does not match)\n" % team)
				continue
			print "Autocorrected %s to %s (Team: %s)" % (old_title, tmp_title, team)
			old_title = tmp_title
		if new_title not in mapping and team != 'LoneWizard' and team != 'Rystlnix':
			tmp_title = funcs.spelling_correction(new_title)
			if tmp_title == "": # no correction possible
				e.write("%s - invalid swap request (bench title does not match)\n" % team)
				continue
			print "Autocorrected %s to %s (Team: %s)" % (new_title, tmp_title, team)
			new_title = tmp_title

		# both titles match
		'''
		if team == 'LoneWizard':
			print "skthello"
			old_title = 'WWW.Working!!'
		elif team == 'Rystlnix':
			print "skthello2"
			old_title = 'Luger Code 1951'

		if team == 'LoneWizard':
			new_title = 'Drifters'
		elif team == 'Rystlnix':
			new_title = 'WWW.Working!!'
		'''



		old_id = mapping[old_title]
		new_id = mapping[new_title]

		team_ids = [z[0] for z in teams[team]]
		bench_ids = [z[0] for z in bench[team]]

		# both titles are in the active team and bench
		if old_id in team_ids and new_id in bench_ids:
			teams[team][team_ids.index(old_id)] = tuple((new_id, new_title))
			bench[team][bench_ids.index(new_id)] = tuple((old_id, old_title))
			swaps[team][0] -= 1
			swaps[team][1] = swap_delay
			made_swaps.append(team)

		# title not in active team or bench
		if old_id not in team_ids:
			e.write("%s - invalid swap request (title not in active team)\n" % team)
		if new_id not in bench_ids:
			e.write("%s - invalid swap request (title not on bench)\n" % team)

	return (teams, bench, swaps)


def determine_aces(aces, teams, t_scores, a_scores, anime, mapping, e):
	"""
	Processes aces.

	@param aces aces dictionary
	@param teams teams dictionary
	@param t_scores team score dictionary (bonus/penalties)
	@param a_scores anime score dictionary
	@param mapping {a_title:a_id} mapping
	@param e writer for errors

	@return tuple of changed (aces, teams, t_scores)
	"""

	aces, new_aces = get_aces(aces, teams, anime, mapping, e)
	for team, ace in new_aces:
		print "%s \n" % team
		#print "%s \n" % ace
		#print aces[team]
		# all active anime for the team (get a_id's) (remove all titles with 40k+ watching+completed)
		team_anime = [a[0] for a in teams[team] if (anime[a[0]][3][0]+anime[a[0]][3][1]) <= ace_cutoff]
		# all scores for the active anime (remove all titles with 40k+ watching+completed)
		points = [a_scores[a_id][1] for a_id in team_anime if (anime[a_id][3][0]+anime[a_id][3][1]) <= ace_cutoff]

		ace = correct_title(ace)
		if ace not in team_anime: # when ace is on bench
			t_scores[team][1] -= 3000
			continue
		if points[team_anime.index(ace)] == max(points):
			t_scores[team][1] += 3000
			print "xx"
		else:
			t_scores[team][1] -= 3000
	return (aces, teams, t_scores)


def init_data():
	"""
	Initializes all data structures in week 1.
	"""

	path = "lists/"
	teams = {}
	f = [line.strip() for line in open("%steam_list.txt" % path).readlines()\
			 if not re.search("^\s+$", line)] # reads team_name + (IDs + titles)
	for line in f:
		if line.startswith("Team:"):
			team_name = line[6:]
			teams[team_name] = []
		else:
			a_id = line.split()[0]
			a_title = " ".join(line.split()[1:])
			teams[team_name].append(tuple((a_id, a_title)))
	swaps = {team_name: [swap_number, 0] for team_name in teams.keys()} # [no. of swaps left, time delay 0 = swap possible]
	aces = {team_name: [] for team_name in teams.keys()} # list of used aces
	wildcards = {team_name: "" for team_name in teams.keys()} # used wildcard
	series = re.findall('(\d+)\s(.+)', open("%sanime_list.txt" % path).read())
	# data structure for anime:
	# anime = {anime ID : title, [all_posts, new_posts], team count, [watch, compl, drop, score, favs], [all_threads, new_threads],
	# [[simulcasts], simulcast_score], license]}
	anime = {a_id: [a_title.strip(), [0, 0], 0, [], [0, 0], [[],0], 0] for a_id, a_title in series}
	a_scores = {a_id: [0, 0] for a_id in anime.keys()} # all_score, curr_score
	t_scores = {team_name: [0, 0, 0, 0] for team_name in teams.keys()} # all, current, rank, unique score (week)

	funcs.save_all_data(week-1, teams, swaps, aces, wildcards,\
		anime, a_scores, t_scores) # saves all initialized data structures


# ----------------------------------------------------------------------------
# MAIN FUNCTIONS
# ----------------------------------------------------------------------------


def main(retrieve=True):
	"""
	Main function of the scorer.
	"""

	mapping = funcs.map_anime()
	httpconn = httplib.HTTPSConnection("myanimelist.net")
	e = funcs.open_out_file(week, "errors")

	# inizialize all data structures in week 1
	if week == 1:
		init_data()


	# load all data structures from the week before, including name changes
	teams, swaps, aces, wildcards, anime, a_scores, t_scores = funcs.load_all_data(week-1)

	# set current team scores to 0
	for team in t_scores:
		t_scores[team][1] = 0

	#for pre-run points deductions
	'''
	for team in teams:
		for borked_anime in teams[team][:5]:
			b_title = borked_anime[1]
			if b_title == 'Anima Yell!':
				print b_title
				t_scores[team][1] -= 1562
			if b_title == 'Hinomaruzumou':
				print b_title
				t_scores[team][1] -= 7518
			if b_title == 'Kaze ga Tsuyoku Fuiteiru':
				print b_title
				t_scores[team][1] -= 12387
			if b_title == 'Release the Spyce':
				print b_title
				t_scores[team][1] -= 4253
			if b_title == 'RErideD: Tokigoe no Derrida':
				print b_title
				t_scores[team][1] -= 6854
			if b_title == 'SSSS.Gridman':
				print b_title
				t_scores[team][1] -= 7316
			if b_title == 'Uchi no Maid ga Uzasugiru!':
				print b_title
				t_scores[team][1] -= 9740
			if b_title == 'Ulysses: Jehanne Darc to Renkin no Kishi':
				print b_title
				t_scores[team][1] -= 3343
	print t_scores
	'''

	# extract bench titles
	bench = {team_name: [a_titles.pop() for i in range(bench_len)][::-1] for team_name, a_titles in teams.items()}
	# extended slices http://docs.python.org/release/2.3.5/whatsnew/section-slices.html


	# start using wildcards in week X
	wildcards, t_scores, swaps = use_wildcards(wildcards, t_scores, swaps, e)


	# make swaps

	#teams, swaps, _, _, _, _, _ = funcs.load_all_data(week)
	#bench = {team_name: [a_titles.pop() for i in range(bench_len)][::-1] for team_name, a_titles in teams.items()}

	teams, bench, swaps = make_swaps(teams, bench, swaps, anime, mapping, httpconn, e)

	# count the number of teams for every anime (active team only, not bench)
	flat_list = [item for sublist in teams.values() for item in sublist]
	for a_id in anime:
		anime[a_id][2] = sum([1 for x in flat_list if x[0] == a_id])


	# calculate scores for every anime entry
	if retrieve:
		for a_id, a_info in anime.items():
			score, new_posts, detailed_info, new_threads = get_score(a_id, a_info, week, httpconn)
			anime[a_id][1][0] += new_posts # add new posts to all posts
			anime[a_id][1][1] = new_posts # set current posts
			anime[a_id][3] = detailed_info # set detailed info
			anime[a_id][4][0] += new_threads # add new posts to all posts
			anime[a_id][4][1] = new_threads # set current posts
			a_scores[a_id][1] = score # set current score

	# use existing scores for the given week (if you need to fix errors like missing aces)
	else:
		_, _, _, _, anime, a_scores, _ = funcs.load_all_data(week)

	#change totals; subtract current current scores
	if not retrieve:
		for a_id in a_scores:
			a_scores[a_id][0] -= a_scores[a_id][1]

	# follow the format of the below code to make changes to discussion posts when retrieve == False
	'''
	anime['33985'][1][0] -= 87
	anime['33985'][1][1] -= 87
	a_scores['33985'][1] -= 87*25

	anime['33041'][1][0] -= 38
	anime['33041'][1][1] -= 38
	a_scores['33041'][1] -= 38*25

	anime['33572'][1][0] -= 3
	anime['33572'][1][1] -= 3
	a_scores['33572'][1] -= 3*25

	anime['33299'][1][0] -= 5
	anime['33299'][1][1] -= 5
	a_scores['33299'][1] -= 5*25

	anime['33003'][1][0] -= 138
	anime['33003'][1][1] -= 138
	a_scores['33003'][1] -= 138*25

	anime['33051'][1][0] -= 40
	anime['33051'][1][1] -= 40
	a_scores['33051'][1] -= 40*25

	anime['31631'][1][0] -= 17
	anime['31631'][1][1] -= 17
	a_scores['31631'][1] -= 17*25

	anime['32603'][1][0] -= 37
	anime['32603'][1][1] -= 37
	a_scores['32603'][1] -= 37*25

	anime['32038'][1][0] -= 5
	anime['32038'][1][1] -= 5
	a_scores['32038'][1] -= 5*25

	anime['33433'][1][0] -= 192
	anime['33433'][1][1] -= 192
	a_scores['33433'][1] -= 192*25

	anime['32881'][1][0] -= 39
	anime['32881'][1][1] -= 39
	a_scores['32881'][1] -= 39*25

	anime['33023'][1][0] -= 21
	anime['33023'][1][1] -= 21
	a_scores['33023'][1] -= 21*25

	anime['31178'][1][0] -= 27
	anime['31178'][1][1] -= 27
	a_scores['31178'][1] -= 27*25

	anime['33589'][1][0] -= 31
	anime['33589'][1][1] -= 31
	a_scores['33589'][1] -= 31*25

	anime['33094'][1][0] -= 104
	anime['33094'][1][1] -= 104
	a_scores['33094'][1] -= 104*25
	'''

	# simulcasts
	if week in fansub_week:
		print "fetching simuls"
		old_scores = {a_id: a_info[5][1] for (a_id, a_info) in anime.items()} # store old information for not retrieve case
		anime = get_fansubs(anime, mapping, retrieve)
		for a_id, a_info in anime.items():
			if not retrieve:
				a_scores[a_id][1] -= old_scores[a_id]
			a_scores[a_id][1] += a_info[5][1]


	# licenses
	if week == license_week:
		anime = get_licenses(anime, mapping)
		for a_id, a_info in anime.items():
			a_scores[a_id][1] += a_info[6] * 10000


	# assign anime scores to users
	for team in teams:
		print team
		for a_id in [a[0] for a in teams[team]]:
			print a_id
			t_scores[team][1] += a_scores[a_id][1]


	# process aces
	aces, teams, t_scores = determine_aces(aces, teams, t_scores, a_scores, anime, mapping, e)


	# apply highest unique score
	last = 0
	sorted_highest = sorted(t_scores.items(), key=lambda x:x[1][1], reverse=True)
	for x in sorted_highest[:5]:
		print x
	for i, (team, (_, points, _, received)) in enumerate(sorted_highest):
		print i, team, points, sorted_highest[i+1][1][1]
		if points == last:
			continue
		# several teams have the same weekly score
		if points == sorted_highest[i+1][1][1]:
			last = points
			continue
		# team has already received unique bonus
		if received > 0:
			last = points
			continue
		# apply bonus to the team
		t_scores[team][1] += 4000
		t_scores[team][3] = week
		break


	# add new scores to all scores
	#old_a_scores = {a_id: scores[1] for (a_id, scores) in a_scores.items()} # store old information for not retrieve case
	for a_id in a_scores:
		a_scores[a_id][0] += a_scores[a_id][1]
		#if not retrieve:
			#a_scores[a_id][0] -= old_a_scores[a_id]
	for team in teams:
		t_scores[team][0] += t_scores[team][1]


	# add bench titles back to team
	for team in teams:
		teams[team].extend(bench[team])


	# get new ranking and add it to t_scores
	ranking = get_ranking(t_scores)
	for team, rank in ranking.items():
		t_scores[team][2] = rank


	# save all data structures for the current week
	#print aces
	funcs.save_all_data(week, teams, swaps, aces, wildcards, anime, a_scores, t_scores, retrieve)
	if e:
		e.close()
