# -*- coding: cp1252 -*-
import urllib
import time
import random

teams = [user.split("=")[0].strip() for user in open("banners-input.txt").readlines()]
types = "cinderella eromanga eromanga1 saenai2 shingeki2 zero".split()

for team in teams:
  print team
  for typex in types:
    print "     ",typex
    urllib.urlopen("http://mfal.website/falbanners/falbanner.php?type=%s&user=%s" % (typex, team))
    time.sleep(random.randint(5,15))
