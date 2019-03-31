from __future__ import annotations

import configparser
from typing import TYPE_CHECKING, Dict, Union, List, cast

import jikanpy

from fal.clients.mfalncfm_main import session_scope
from fal.models import AnimeWeeklyStat, Season, Anime

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

config = configparser.ConfigParser()
config.read("config.ini")


def get_forum_posts(anime: Anime) -> int:
    '''Not yet implemented'''
    return 0


def get_anime_stats_from_jikan(anime: Anime) -> Dict[str, Union[int, float]]:
    '''
    Makes requests to Jikan given an anime id
    and returns a Dict containing all the information needed to
    populate an AnimeWeeklyStat object
    '''

    jikan = jikanpy.Jikan()
    general_anime_info = jikan.anime(anime.id)
    jikan_anime_stats = jikan.anime(anime.id, extension='stats')

    return {
        'watching': jikan_anime_stats['watching'],
        'completed': jikan_anime_stats['completed'],
        'dropped': jikan_anime_stats['dropped'],
        'score': general_anime_info['score'],
        'favorites': general_anime_info['favorites'],
        'forum_posts': get_forum_posts(anime)
    }


def populate_anime_weekly_stats() -> None:
    '''
    Populates the AnimeWeeklyStat table with a row for each anime
    using data from Jikan.
    '''

    season_of_year = config.get("season info", "season").lower()
    year = config.getint("season info", "year")
    week = config.getint("weekly info", "current-week")

    with session_scope() as session:
        anime_list = Season.get_season_from_database(
            season_of_year, year, session).anime

        # casting until update in sqlalchemy-stubs
        for anime in cast(List[Anime], anime_list):
            stat_data = get_anime_stats_from_jikan(anime)
            stat_data.update({
                'week': week,
                'anime_id': anime.id
            })

            query = session.query(AnimeWeeklyStat). \
                filter(AnimeWeeklyStat.week == week,
                       AnimeWeeklyStat.anime_id == anime.id)
            anime_weekly_stat = query.one_or_none()

            if not anime_weekly_stat:
                anime_weekly_stat = AnimeWeeklyStat()

            for key, value in stat_data.items():
                setattr(anime_weekly_stat, key, value)

            session.add(anime_weekly_stat)
