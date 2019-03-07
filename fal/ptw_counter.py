from __future__ import annotations

from fal.clients.mfalncfm_main import session_scope
from fal.models import PlanToWatch, Anime
from fal.collect_series import get_season_from_database

from jikanpy import Jikan

import configparser
import csv
import time
from collections import namedtuple
from datetime import date
from pprint import pprint
from typing import List, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

PTWEntry = namedtuple('PTWEntry', 'title id ptw_count')


def localize_number(num: int) -> str:
    """Add commas to integer at every thousands place"""
    return '{:,}'.format(num)


def get_ptw_info(anime_list: Iterable[Anime]) -> List[PTWEntry]:
    """Store PTW of each anime in a list of tuples"""
    jikan = Jikan()
    ptw = list()
    for anime in anime_list:
        anime_stats = jikan.anime(anime.id, extension='stats')  # type: ignore
        anime_ptw_num = localize_number(anime_stats['plan_to_watch'])
        ptw.append(PTWEntry(anime.name, anime.id, anime_ptw_num))
        time.sleep(5)
    return ptw


def output_ptw_info(season_of_year: str, year: int, ptw: Iterable[PTWEntry], directory: str) -> None:
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
    """Adds or updates Plan To Watch entry to database"""
    query = session.query(PlanToWatch). \
        filter(PlanToWatch.anime_id == anime_id, PlanToWatch.date == date)
    ptw_entry = query.one_or_none()

    if ptw_entry:
        ptw_entry.count = ptw_count
        print(f'Updating {ptw_entry} in database')
        session.commit()
    else:
        ptw_entry = PlanToWatch(anime_id=anime_id, date=date, count=ptw_count)
        print(f'Adding {ptw_entry} to database')
        session.add(ptw_entry)


def ptw_counter() -> None:
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Ensure season is lowercase string and year is integer
    season_of_year = config["season info"]["season"].lower()
    year = int(config["season info"]["year"])

    today = date.today()

    # Database workflow
    with session_scope() as session:
        season = get_season_from_database(season_of_year, year, session)
        query = session.query(Anime).filter(Anime.season_id == season.id)
        anime_list = query.all()
        print(f'Length of list of anime: {len(anime_list)}')

        # Store PTW of each anime in a list of tuples
        ptw = get_ptw_info(anime_list)
        pprint(ptw)
        output_ptw_info(season_of_year, year, ptw, 'ptw_csv')

        print('Adding PTW entries to PTW table')
        for entry in ptw:
            ptw_count = int(entry.ptw_count.replace(',', ''))
            add_ptw_to_database(entry.id, today, ptw_count, session)
