from jikanpy import Jikan
from pprint import pprint
from datetime import date
import time
import csv

from fal.collect_series import add_anime_to_database

import configparser


def get_tv_anime(season_info):
    """Return list of TV anime objects from season info"""
    tv_anime = list()
    for anime in season_info['anime']:
        if anime['type'] == 'TV':
            tv_anime.append(anime)
    return tv_anime


def localize_number(num):
    """Add commas to integer at every thousands place"""
    return '{:,}'.format(num)


def output_ptw_info(season, year, ptw):
    """Outputs PTW info to CSV file"""
    today = str(date.today())
    filename = f'ptw_csv/{season}-{year}-{today}.csv'
    with open(filename, 'w', encoding='utf8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(sorted(ptw))
    print(f'Outputted PTW info to {filename}')


def ptw_counter():
    jikan = Jikan()

    config = configparser.ConfigParser()
    config.read("config.ini")

    # Ensure season is lowercase string and year is integer
    season_of_year = config["season info"]["season"].lower()
    year = int(config["season info"]["year"])

    # Get list of anime in the season
    season_info = jikan.season(year=year, season=season_of_year)
    assert season_info['season_name'].lower() == season_of_year
    assert season_info['season_year'] == year

    anime_list = get_tv_anime(season_info)
    print(f'Length of list of anime: {len(anime_list)}')

    # Store PTW of each anime in a list of tuples
    ptw = list()
    for anime in anime_list:
        anime_stats = jikan.anime(anime['mal_id'], extension='stats')
        anime_ptw_num = localize_number(anime_stats['plan_to_watch'])
        ptw.append((anime['title'], anime['mal_id'], anime_ptw_num))
        time.sleep(5)
    pprint(ptw)

    output_ptw_info(season_info['season_name'], str(year), ptw)

    # Database workflow
    print('Adding anime to database if not present and adding to PTW table')
