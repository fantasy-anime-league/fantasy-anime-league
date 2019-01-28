infile = "registration.txt"
outfile = "lists/team_headcount.txt"
team_list = []

with open(infile) as inf, open(outfile) as outf:
	for line in inf:
		if "Team:" in line:
			print line
			team_list.append((line.split(": ")[1]).split("\n")[0])
	print team_list
	for line in outf:
		if "[b]" in line:
			temp = (line.split("[b]")[1]).split("[/b]")[0]
			print temp
		
		
			if temp in team_list:
				team_list.remove(temp)

	print team_list