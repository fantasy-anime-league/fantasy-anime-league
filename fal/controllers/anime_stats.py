from __future__ import annotations

import configparser
import re
import time
import dataclasses
from typing import Dict, Union, List, Any, cast, Optional

import jikanpy

from fal.clients.mfalncfm_main import session_scope
from fal.models import AnimeWeeklyStat, Season, Anime

config = configparser.ConfigParser()
config.read("config.ini")

@dataclasses.dataclass()
class AnimeStats:
    watching: int
    completed: int
    dropped: int
    score: Optional[float]
    favorites: int
    forum_posts: int
    total_points: int = dataclasses.field(init=False)
    week: int = dataclasses.field(init=False)
    anime_id: int = dataclasses.field(init=False)

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

    assert anime.name is not None
    name = anime.name  # https://github.com/python/mypy/issues/4297

    episode_discussions = [thread for thread in forum_threads if re.fullmatch(
        name + r' Episode \d{1,2} Discussion',
        thread['title']
    )]

    if len(episode_discussions) < week:
        print(f"""
            WARNING: did not find as many episode discussion threads for
                {anime.name} as the number of weeks we're in. Double check that
                    this is expected and manually update if necessary.
            """)

        if not episode_discussions:
            return 0

    return sum([disc['replies'] for disc in episode_discussions])


def get_anime_stats_from_jikan(anime: Anime) -> AnimeStats:
    '''
    Makes requests to Jikan given an anime id
    and returns a Dict containing all the information needed to
    populate an AnimeWeeklyStat object
    '''

    jikan = jikanpy.Jikan()
    general_anime_info = jikan.anime(anime.id)
    jikan_anime_stats = jikan.anime(anime.id, extension='stats')

    return AnimeStats(
        watching = jikan_anime_stats['watching'],
        completed = jikan_anime_stats['completed'],
        dropped = jikan_anime_stats['dropped'],
        score = general_anime_info['score'],
        favorites = general_anime_info['favorites'],
        forum_posts = get_forum_posts(anime)
    )

def calculate_anime_weekly_points(stat_data: AnimeStats) -> int:
    '''
    Calculate the points for the week for the anime based on the stats
    '''
    points = 0
    points += (stat_data.watching
             + stat_data.completed
             + config.getint('scoring.dropped', str(stat_data.week), fallback=0) * stat_data.dropped
             + int(config.getint('scoring.anime_score', str(stat_data.week), fallback=0) * stat_data.score)             + config.getint('scoring.favorite', str(stat_data.week), fallback=0) * stat_data.favorites
             + config.getint('scoring info', 'forum-post-multiplier') * stat_data.forum_posts
    )
    # TODO: add scoring for simulcasts and licensing

    return points



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
            print(f"Populating stats for {anime}")
            stat_data = get_anime_stats_from_jikan(anime)
            stat_data.week = week
            stat_data.anime_id = anime.id

            if stat_data.score is None:
                # did not start airing yet
                stat_data.total_points = 0
            else:
                stat_data.total_points = calculate_anime_weekly_points(stat_data)

            anime_weekly_stat = AnimeWeeklyStat()
            for key, value in dataclasses.asdict(stat_data).items():
                setattr(anime_weekly_stat, key, value)

            session.merge(anime_weekly_stat)
            #session.commit()
            time.sleep(config.getint("jikanpy", "request-interval"))
