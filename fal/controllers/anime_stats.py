from __future__ import annotations

import configparser
import dataclasses
import math
import re
import time
from typing import Dict, Union, List, Any, cast, Optional, Iterable, Sequence, Set

import jikanpy
from sqlalchemy import func

from fal.clients.mfalncfm_main import session_scope
from fal.orm import AnimeWeeklyStat, Season, Anime, TeamWeeklyAnime, Team

config = configparser.ConfigParser()
config.read("config.ini")


@dataclasses.dataclass()
class AnimeStats:
    watching: int
    completed: int
    dropped: int
    score: float
    favorites: int
    forum_posts: int
    total_points: int = dataclasses.field(init=False)
    week: int = dataclasses.field(init=False)
    anime_id: int = dataclasses.field(init=False)


def get_forum_posts(anime: Anime) -> int:
    """
    Requests forum posts from Jikan, then sums up all the episode discussion
    thread replies.

    Where N is the weekly interval forum posts are scored:
        if this week is not a multiple of N, return 0
        Otherwise:
            Gathers all the posts in the forum discussion threads of the past N weeks,


    Currently uses regex to match for Episode Discussion. This is brittle and
    will stop working once we get over 15 forum threads on an anime.

    ASAP we should fix Jikan's API so that it can filter for episode discussion threads
    in its search. Alternatively, we could remove the 15 search result limit but that
    seems harder to do.

    Also TODO: add functionality to subtract a certain number of forum posts,
    i.e. posts made before season started
    """

    week = config.getint("weekly info", "current-week")
    n_week = config.getint("scoring info", "forum-posts-every-n-weeks")

    # don't score forum posts if this isn't the right week
    if week % n_week != 0:
        return 0

    jikan = jikanpy.Jikan()
    forum_threads: List[Dict[str, Any]] = jikan.anime(anime.id, extension="forum")[
        "topics"
    ]

    or_alias = ""
    if anime.alias:
        or_alias = f"|{anime.alias}"

    # here we build the regex OR statement based on all the week numbers
    # since the last time we checked forum posts
    episode_nums_str = "|".join(
        [str(num) for num in range(max(1, week - n_week + 1), week + 1)]
    )

    episode_discussions = [
        thread
        for thread in forum_threads
        if re.fullmatch(
            f"({anime.name}{or_alias}) Episode ({episode_nums_str}) Discussion",
            thread["title"],
        )
    ]

    if not episode_discussions:
        print(
            f"""
            WARNING: did not find as many episode discussion threads for {anime.name}.
            Double check that this is expected and manually update if necessary.
            (Found {len(episode_discussions)} discussions in the {n_week} weeks
            before week {week})
            """
        )

    return sum([disc["replies"] for disc in episode_discussions])


def get_anime_stats_from_jikan(anime: Anime) -> AnimeStats:
    """
    Makes requests to Jikan given an anime id
    and returns a Dict containing all the information needed to
    populate an AnimeWeeklyStat object
    """

    jikan = jikanpy.Jikan()
    general_anime_info = jikan.anime(anime.id)
    jikan_anime_stats = jikan.anime(anime.id, extension="stats")

    return AnimeStats(
        watching=jikan_anime_stats["watching"],
        completed=jikan_anime_stats["completed"],
        dropped=jikan_anime_stats["dropped"],
        score=general_anime_info.get("score", 0),
        favorites=general_anime_info["favorites"],
        forum_posts=get_forum_posts(anime),
    )


def calculate_anime_weekly_points(
    stat_data: AnimeStats,
    num_teams_owned_active: int,
    double_score_max_num_teams: int,
    num_regions: int,
    is_licensed: bool,
) -> int:
    """
    Calculate the points for the week for the anime based on the stats
    """
    score_multiplier = 2 if num_teams_owned_active <= double_score_max_num_teams else 1
    points = (
        (stat_data.watching + stat_data.completed) * score_multiplier
        + config.getint("scoring.dropped", str(stat_data.week), fallback=0)
        * stat_data.dropped
        + config.getint("scoring.favorite", str(stat_data.week), fallback=0)
        * stat_data.favorites
        + config.getint("scoring info", "forum-post-multiplier") * stat_data.forum_posts
    )

    # multiplying by None type produces weird results
    # so we do these calculations only if stat_data.score exists
    if stat_data.score:
        points += int(
            config.getint("scoring.anime_score", str(stat_data.week), fallback=0)
            * stat_data.score
        )

    # simulcast
    points += (
        config.getint("scoring.simulcast", str(stat_data.week), fallback=0)
        * num_regions
    )

    # licensing
    if is_licensed:
        points += config.getint("scoring.license", str(stat_data.week), fallback=0)

    return points


def is_week_to_calculate(config_key: str, week: int) -> bool:
    """
    Checks if it is the right week to calculate points for the extra feature
    in the config
    """
    return config.get(config_key, str(week), fallback="No points") is not "No points"


def get_anime_simulcast_region_counts(
    simulcast_lines: Optional[Iterable[str]]
) -> Dict[int, int]:
    print("Getting region counts of each anime in simulcast file")
    anime_simulcast_region_counts = {}
    if simulcast_lines is not None:
        with session_scope() as session:
            for line in simulcast_lines:
                title, subs = line.split("=")
                title = title.strip()
                anime = Anime.get_anime_from_database_by_name(title, session)
                if anime is None:
                    print(f"{title} is not found in database")
                else:
                    num_regions = len(
                        [entry for entry in subs.split() if entry == "simul"]
                    )
                    anime_simulcast_region_counts[anime.id] = num_regions
    return anime_simulcast_region_counts


def get_licensed_anime(licenses_lines: Optional[Iterable[str]]) -> Set[int]:
    print("Getting licensed anime from licenses file")
    licensed_anime = set()
    if licenses_lines is not None:
        with session_scope() as session:
            for title in licenses_lines:
                anime = Anime.get_anime_from_database_by_name(title.strip(), session)
                if anime is None:
                    print(f"{title} is not found in database")
                else:
                    licensed_anime.add(anime.id)
    return licensed_anime


def populate_anime_weekly_stats(
    simulcast_lines: Optional[Iterable[str]] = None,
    licenses_lines: Optional[Iterable[str]] = None,
) -> None:
    """
    Populates the AnimeWeeklyStat table with a row for each anime
    using data from Jikan.
    """

    season_of_year = config.get("season info", "season").lower()
    year = config.getint("season info", "year")
    week = config.getint("weekly info", "current-week")

    if is_week_to_calculate("scoring.simulcast", week) and simulcast_lines is None:
        raise ValueError(f"simulcast file is required for week {week}")
    if is_week_to_calculate("scoring.license", week) and licenses_lines is None:
        raise ValueError(f"licenses file is required for week {week}")

    anime_simulcast_region_counts = get_anime_simulcast_region_counts(simulcast_lines)
    licensed_anime = get_licensed_anime(licenses_lines)

    with session_scope() as session:
        season = Season.get_season_from_database(season_of_year, year, session)
        anime_list = cast(Iterable[Anime], season.anime)

        anime_ids_collected = [
            row[0]
            for row in session.query(AnimeWeeklyStat.anime_id)
            .join(Anime)
            .filter(AnimeWeeklyStat.week == week)
            .filter(Anime.season_id == season.id)
            .all()
        ]

        if anime_ids_collected:
            action = input(
                "At least some anime stats have been collected for this week"
                " already. How should we proceed (overwrite/collect-missing/abort)?"
            )
            if action == "collect-missing":
                anime_list = (
                    anime for anime in anime_list if anime.id not in anime_ids_collected
                )
            elif action == "overwrite":
                pass
            else:
                return

        # for each anime, get the number of teams that have it on active
        anime_active_counts = dict(
            session.query(Anime.id, func.count("*"))
            .join(TeamWeeklyAnime.anime)
            .filter(TeamWeeklyAnime.week == week)
            .filter(Anime.season_id == season.id)
            .filter(TeamWeeklyAnime.bench == 0)
            .group_by(Anime.id)
            .all()
        )
        double_score_max_num_teams = math.floor(
            config.getint("scoring info", "percent-ownership-for-double-score")
            / 100
            * len(cast(Sequence[Team], season.teams))
        )

        # casting until update in sqlalchemy-stubs
        for anime in cast(List[Anime], anime_list):
            print(f"Populating stats for {anime}")
            try:
                stat_data = get_anime_stats_from_jikan(anime)
            except jikanpy.exceptions.APIException as e:
                print(
                    f"Jikan servers did not handle our request very well, skipping: {e}"
                )
                continue

            if (
                is_week_to_calculate("scoring.simulcast", week)
                and anime.id not in anime_simulcast_region_counts
            ):
                print(
                    f"{anime.id}-{anime.name} doesn't have an entry in simulcast file"
                )

            stat_data.week = week
            stat_data.anime_id = anime.id
            stat_data.total_points = calculate_anime_weekly_points(
                stat_data,
                anime_active_counts[anime.id],
                double_score_max_num_teams,
                anime_simulcast_region_counts.get(anime.id, 0),
                anime.id in licensed_anime,
            )

            anime_weekly_stat = AnimeWeeklyStat()
            for key, value in dataclasses.asdict(stat_data).items():
                setattr(anime_weekly_stat, key, value)

            session.merge(anime_weekly_stat)
            time.sleep(config.getint("jikanpy", "request-interval"))
