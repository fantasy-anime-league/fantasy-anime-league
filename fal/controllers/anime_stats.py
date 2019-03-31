from __future__ import annotations

import configparser
import functools
import re
from typing import Dict, Union, List, Any, cast

import jikanpy

from fal.clients.mfalncfm_main import session_scope
from fal.models import AnimeWeeklyStat, Season, Anime

config = configparser.ConfigParser()
config.read("config.ini")


def get_forum_posts(anime: Anime) -> int:
    '''
    Requests forum posts from Jikan, then sums up all the episode discussion
    thread replies

    Currently uses regex to match for Episode Discussion. This is brittle and
    will stop working once we get over 15 forum threads on an anime.

    ASAP we should fix Jikan's API so that it can filter for episode discussion threads
    in its search. Alternatively, we could remove the 15 search result limit but that
    seems harder to do.
    '''
    week = config.getint("weekly info", "current-week")
    jikan = jikanpy.Jikan()
    forum_threads: List[Dict[str, Any]] = jikan.anime(
        anime.id, extension='forum')['topics']

    episode_discussions = list(filter(
        lambda thread: re.fullmatch(
            anime.name + r' Episode \d{1,2} Discussion',
            thread['title']
        ),
        forum_threads
    ))

    if len(episode_discussions) < week:
        print(f"""
            WARNING: did not find as many episode discussion threads for \
                {anime.name} as the number of weeks we're in. Double check that \
                    this is expected and manually update if necessary.
            """)

    return functools.reduce(
        lambda accm, episode_discussion: accm + episode_discussion['replies'],
        episode_discussions,
        0
    )


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

            anime_weekly_stat = AnimeWeeklyStat()
            for key, value in stat_data.items():
                setattr(anime_weekly_stat, key, value)

            session.merge(anime_weekly_stat)
