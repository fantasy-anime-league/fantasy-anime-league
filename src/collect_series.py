#!/usr/bin/python3.7

from clients import mfalncfm_main

import funcs
import re
import requests
import configparser

config = configparser.ConfigParser()


def get_series(search_url):
    """Retrieve a list of (anime_id, anime_title) from a MAL advanced search URL.

    Arguments:
        search_url: the MAL advanced search URL, with the value of the `show`
            query parameter being `%i`

    Returns:
        A list of tuples representing (anime_id, anime_title). For example:

        ('25879', 'Working!!!')
    """
    series = []
    headers = dict(config['myanimelist.net request header'].items())

    with mfalncfm_main.Client() as cursor:
        cursor.execute(
            'SELECT secret.`key`, secret.value FROM secret WHERE secret.context="myanimelist.net request header"')

        for (key, value) in cursor:
            headers[key] = value

    for show in [0, 20]:
        r = requests.get(search_url.format(show), headers=headers)
        res = r.text
        series.extend(re.findall(r'"/anime/(\d+)/(.+?)"', res))
    return list(set(series))


def main():
    config.read('config.ini')
    SERIES = get_series(config['myanimelist.net']['advanced search url'])
    SERIES_TXT = open("series.txt", "w")
    SERIES_SORTED_TXT = open("series_sorted.txt", "w")

    for a_id, a_title in sorted(SERIES):
        SERIES_TXT.write("%s %s\n" % (a_id, a_title.replace("_", " ")))

    for a_id, a_title in sorted(SERIES, key=lambda x: x[1]):
        SERIES_SORTED_TXT.write("%s\n" % a_title.replace("_", " "))

    print(len(SERIES))

    SERIES_TXT.close()
    SERIES_SORTED_TXT.close()


if __name__ == "__main__":
    main()
