# check_usernames.py
# FAL (Fantasy Anime League)
# http://myanimelist.net/clubs.php?cid=379
# (c) 2012-2015, Luna_ (luna.myanimelist@gmail.com)

import re
import urllib
import time
import httplib
import gzip
import StringIO


def get_header():
    my_cookie = """gn_country=US;
        __utma=242346526.1895944832.1317205945.1317205945.1317205945.1;
        __utmb=242346526.4.10.1317205945;
        __utmc=242346526;
        __utmz=242346526.1317205945.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"""

    headers = {
        'User-Agent': 'api-fal-d3972acfea932b40a96066c9cfc327e0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive': '115',
        'Connection': 'keep-alive',
        'Referer': 'http://myanimelist.net/forum/?clubid=379',
        'Cookie': '%s' % my_cookie
    }

    postdata = {}

    params = urllib.urlencode(postdata)

    return (params, headers)


def check(name):
    print name
    params, headers = get_header()
    httpconn = httplib.HTTPConnection("myanimelist.net")
    httpconn.connect()
    httpconn.request("GET", "/profile/%s" % name, params, headers)
    response = httpconn.getresponse()
    if response.getheader("Content-Encoding") == "gzip":
        res = gzip.GzipFile(fileobj=StringIO.StringIO(response.read())).read()
    else:
        res = response.read()
    httpconn.close()
    profile_name = re.findall("</div>(.+?)'s Profile</h1>", res)
    if len(profile_name) > 0:
        profile_name = re.findall("</div>(.+?)'s Profile</h1>", res)[0]
    else:
        print "username doesn't exist anymore: ", name
    if name != profile_name:
        print "profile name: ", profile_name
        print "our name: ", name
        print ""


def main():
    f_name = "../lists/team_headcount.txt"
    names = re.findall(r"\[b\](.+?)\[/b\]\n", open(f_name).read())

    # best to check in batches of about 100 users, to avoid too many
    # server accesses in a small amount of time
    for name in names[:100]:
        check(name)
        time.sleep(5)


main()
