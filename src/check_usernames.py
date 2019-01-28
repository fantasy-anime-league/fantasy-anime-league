#!/usr/bin/python3.7

from clients import mfalncfm_main

import re
import requests
import time
import configparser


def check(name):
    print(name)
    config = configparser.ConfigParser()
    config.read('config.ini')

    headers = dict(config['myanimelist.net request header'].items())
    uri = config['myanimelist.net']['profile uri']

    with mfalncfm_main.Client() as cursor:
        cursor.execute(
            'SELECT secret.`key`, secret.value FROM secret WHERE secret.context="myanimelist.net request header"')

        for (key, value) in cursor:
            headers[key] = value
    r = requests.get(f'{uri}{name}', params={}, headers=headers)
    res = r.text

    # TODO: confirm that the profile exists in a more elegant, DOM-aware fashion
    profile_name_matches = re.findall("<title>\n(.+?)&#039;s Profile", res)
    profile_name = None
    if len(profile_name_matches) > 0:
        profile_name = profile_name_matches[0]
    else:
        print("username doesn't exist anymore: ", name)
    if name != profile_name:
        print("profile name: ", profile_name)
        print("our name: ", name)
        print("")


def main():
    f_name = "lists/team_headcount.txt"
    names = re.findall(r"\[b\](.+?)\[/b\]\n", open(f_name).read())

    # best to check in batches of about 100 users, to avoid too many
    # server accesses in a small amount of time
    for name in names[:100]:
        check(name)
        time.sleep(5)


if __name__ == "__main__":
    main()
