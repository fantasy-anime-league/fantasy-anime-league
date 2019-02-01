#!/usr/bin/python3.7

from jikanpy import Jikan
import configparser


def get_series(season, year):
    """Retrieve a list of (anime_id, anime_title) from the season info.

    Arguments:
        season: season to get series from
        year: year to get series from

    Returns:
        A dict from anime_id to anime_title. For example:

        {25879: 'Working!!!'}
    """
    jikan = Jikan()
    # Get list of anime in the season
    season_info = jikan.season(year=year, season=season)
    assert season_info["season_name"].lower() == season
    assert season_info["season_year"] == year

    tv_anime = dict()
    for anime in season_info["anime"]:
        if anime["type"] == "TV":
            tv_anime[anime["mal_id"]] = anime["title"]
    return tv_anime


def output_series(series, filename):
    """Output series ids and titles in the format:

    id_1 title_1
    id_2 title_2
    """
    with open(filename, "w", encoding="utf8") as f:
        f.writelines(f"{a_id} {a_title}\n" for a_id, a_title in sorted(series))


def output_series_titles(titles, filename):
    """Output series titles sorted lexicographically in the format:

    title_1
    title_2
    """
    with open(filename, "w", encoding="utf8") as f:
        f.writelines(f"{title}\n" for title in sorted(titles))


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Ensure season is lowercase string and year is integer
    season = config["season info"]["season"].lower()
    year = int(config["season info"]["year"])

    series_dict = get_series(season, year)
    series = series_dict.items()
    print(len(series))

    output_series(series, "series.txt")
    output_series_titles(series_dict.values(), "series_sorted.txt")


if __name__ == "__main__":
    main()
