#!/usr/bin/python3.7

from jikanpy import Jikan
import configparser

config = configparser.ConfigParser()


def get_series(season_info):
    """Retrieve a list of (anime_id, anime_title) from the season info.

    Arguments:
        season_info: dict containing season info from Jikanpy

    Returns:
        A dict from anime_id to anime_title. For example:

        {25879: 'Working!!!'}
    """
    tv_anime = dict()
    for anime in season_info["anime"]:
        if anime["type"] == "TV":
            tv_anime[anime["mal_id"]] = anime["title"]
    return tv_anime


def output_series(series):
    """Output series ids and titles in the format:

    id_1 title_1
    id_2 title_2
    """
    with open("series.txt", "w", encoding="utf8") as f:
        f.writelines(f"{a_id} {a_title}\n" for a_id, a_title in sorted(series))


def output_series_titles(titles):
    """Output series titles sorted lexicographically in the format:

    title_1
    title_2
    """
    with open("series_sorted.txt", "w", encoding="utf8") as f:
        f.writelines(f"{title}\n" for title in sorted(titles))


def main():
    config.read('config.ini')

    # Ensure season is lowercase string and year is integer
    season = config['myanimelist.net']['season'].lower()
    year = int(config['myanimelist.net']['year'])

    jikan = Jikan()
    # Get list of anime in the season
    season_info = jikan.season(year=year, season=season)
    assert season_info['season_name'].lower() == season
    assert season_info['season_year'] == year

    series_dict = get_series(season_info)
    series = series_dict.items()
    print(len(series))

    output_series(series)
    output_series_titles(series_dict.values())


if __name__ == "__main__":
    main()
