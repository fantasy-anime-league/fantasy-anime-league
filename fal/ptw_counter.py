from __future__ import annotations

from fal.clients.mfalncfm_main import session_scope
from fal.models import PlanToWatch
from fal.collect_series import get_series, get_season_from_database, add_anime_to_database

from jikanpy import Jikan

import configparser
import csv
import time
from datetime import date
from pprint import pprint
from typing import List, Tuple, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def localize_number(num: int) -> str:
    """Add commas to integer at every thousands place"""
    return '{:,}'.format(num)


def get_ptw_info(series_dict: Dict[int, str]) -> List[Tuple[str, int, str]]:
    """Store PTW of each anime in a list of tuples"""
    jikan = Jikan()
    ptw = list()
    for anime_id, anime_title in series_dict.items():
        anime_stats = jikan.anime(anime_id, extension='stats')  # type: ignore
        anime_ptw_num = localize_number(anime_stats['plan_to_watch'])
        ptw.append((anime_title, anime_id, anime_ptw_num))
        time.sleep(5)
    return ptw


def output_ptw_info(season_of_year: str, year: int, ptw: List[Tuple[str, int, str]], directory: str) -> None:
    """Outputs PTW info to CSV file"""
    season_of_year = season_of_year.capitalize()
    year_str = str(year)
    today = str(date.today())
    filename = directory + f'/{season_of_year}-{year_str}-{today}.csv'
    with open(filename, 'w', encoding='utf8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(sorted(ptw))
    print(f'Outputted PTW info to {filename}')


def add_ptw_to_database(anime_id: int, date: date, ptw_count: int, session: Session) -> None:
    """Adds Plan To Watch entry to database"""
    ptw_entry = PlanToWatch(anime_id=anime_id, date=date, count=ptw_count)
    print(f'Adding {ptw_entry} to database')
    session.add(ptw_entry)


def ptw_counter() -> None:
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Ensure season is lowercase string and year is integer
    season_of_year = config["season info"]["season"].lower()
    year = int(config["season info"]["year"])

    series_dict = get_series(season_of_year, year)
    print(f'Length of list of anime: {len(series_dict)}')

    # Store PTW of each anime in a list of tuples
    ptw = get_ptw_info(series_dict)
    pprint(ptw)

    output_ptw_info(season_of_year, year, ptw, 'ptw_csv')

    today = date.today()

    # Database workflow
    print('Adding anime to database if not present and adding to PTW table')
    with session_scope() as session:
        season = get_season_from_database(season_of_year, year, session)
        for entry in ptw:
            anime_title = entry[0]
            anime_id = entry[1]
            anime_ptw_count = int(entry[2].replace(',', ''))
            add_anime_to_database(entry[1], entry[0], season, session)
            add_ptw_to_database(anime_id, today, anime_ptw_count, session)
