from __future__ import annotations

import configparser
import math
import time
from typing import (
    Dict,
    List,
    Any,
    cast,
    Optional,
    Set,
    TYPE_CHECKING,
)

import attr
import jikanpy
from sqlalchemy import func
import sqlalchemy.orm.exc

from fal.orm.mfalncfm_main import session_scope
from fal.models import Anime, Season
from fal import orm
from .base import Controller

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

config = configparser.ConfigParser()
config.read("config.ini")


@attr.s(auto_attribs=True, kw_only=True)
class JikanResults:
    watching: int
    completed: int
    dropped: int
    score: float
    favorites: int
    total_forum_posts: int
    week: int
    anime_id: int
    total_points: Optional[int] = attr.ib(init=False, default=None)



@attr.s(auto_attribs=True, kw_only=True)
class AnimeStats(Controller):
    """
    Populates the AnimeWeeklyStat table with a row for each anime
    using data from Jikan.
    """

    simulcasts_filepath: str
    licenses_filepath: str

    simulcast_lines: Optional[List[str]] = attr.ib(init=False, default=None)
    licenses_lines: Optional[List[str]] = attr.ib(init=False, default=None)

    forum_post_week_interval: int = attr.ib(init=False, default=config.getint("scoring info", "forum-posts-every-n-weeks"))
    forum_post_multipler: int = attr.ib(init=False, default=config.getint("scoring info", "forum-post-multiplier"))
    percent_ownership_for_double_score: int = attr.ib(init=False, default=config.getint("scoring info", "percent-ownership-for-double-score"))
    dropped_multiplier: int = attr.ib(init=False)
    favorite_multiplier: int = attr.ib(init=False)
    anime_score_multipler: int = attr.ib(init=False)
    simulcast_multiplier: int = attr.ib(init=False)
    license_score: int = attr.ib(init=False)


    def is_week_to_calculate(self, config_key: str) -> bool:
        """
        Checks if it is the right week to calculate points for the extra feature
        in the config
        """
        return (
            config.get(config_key, str(self.current_week), fallback="No points") != "No points"
        )

    def _extract_file_contents(self) -> None:
        try:
            with open(self.simulcasts_filepath, encoding="utf-8-sig") as f:
                self.simulcast_lines = f.readlines()
        except IOError:
            if self.is_week_to_calculate("scoring.simulcast"):
                raise ValueError(f"simulcast file is required for week {self.current_week}")

        try:
            with open(self.licenses_filepath, encoding="utf-8-sig") as f:
                self.licenses_lines = f.readlines()
        except IOError:
            if self.is_week_to_calculate("scoring.license"):
                raise ValueError(f"licenses file is required for week {self.current_week}")

    def __attrs_post_init__(self) -> None:
        self._extract_file_contents()

        self.dropped_multiplier = config.getint("scoring.dropped", str(self.current_week), fallback=0)
        self.favorite_multiplier = config.getint("scoring.favorite", str(self.current_week), fallback=0)
        self.anime_score_multipler = config.getint("scoring.anime_score", str(self.current_week), fallback=0)
        self.simulcast_multiplier = config.getint("scoring.simulcast", str(self.current_week), fallback=0)
        self.license_score = config.getint("scoring.license", str(self.current_week), fallback=0)

    def get_total_forum_posts(self, anime: Anime) -> int:
        """
        Requests episode discussion threads from Jikan, then sums up all the thread replies.

        Where N is the weekly interval forum posts are scored:
            if this week is not a multiple of N, return 0
            Otherwise:
                Gathers all the posts in the forum discussion threads of the past N weeks,

        Also TODO: add functionality to subtract a certain number of forum posts,
        i.e. posts made before season started
        """

        jikan = jikanpy.Jikan()
        episode_discussions: List[Dict[str, Any]] = jikan.anime(anime.mal_id, extension="forum/episodes")["topics"]

        if not episode_discussions:
            print(
                f"""
                WARNING: did not find any episode discussion threads for {anime}.
                Double check that this is expected and manually update if necessary.
                """
            )

        return sum([disc["replies"] for disc in episode_discussions])

    def get_anime_stats_from_jikan(self, anime: Anime) -> JikanResults:
        """
        Makes requests to Jikan given an anime id
        and returns a Dict containing all the information needed to
        populate an AnimeWeeklyStat object
        """

        general_anime_info = self.jikan.anime(anime.mal_id)
        jikan_anime_stats = self.jikan.anime(anime.mal_id, extension="stats")

        return JikanResults(
            watching=jikan_anime_stats["watching"],
            completed=jikan_anime_stats["completed"],
            dropped=jikan_anime_stats["dropped"],
            score=general_anime_info.get("score", 0),
            favorites=general_anime_info["favorites"],
            total_forum_posts=self.get_total_forum_posts(anime),
            week=self.current_week,
            anime_id=anime.mal_id
        )

    def calculate_anime_weekly_points(
        self,
        anime: Anime,
        stat_data: JikanResults,
        num_teams_owned_active: int,
        double_score_max_num_teams: int,
        num_regions: int,
        is_licensed: bool,
    ) -> int:
        """
        Calculate the points for the week for the anime based on the stats
        """
        lower_ownership_multiplier = (
            2 if num_teams_owned_active <= double_score_max_num_teams else 1
        )



        # fmt: off
        points = (
            lower_ownership_multiplier * (stat_data.watching + stat_data.completed)
            + self.dropped_multiplier * stat_data.dropped
            + self.favorite_multiplier * stat_data.favorites
            + self.simulcast_multiplier * num_regions
            + self.license_score * int(is_licensed)
        )

        if self.current_week % self.forum_post_week_interval == 0:
            previous_forum_posts = anime.get_forum_posts_for_week(self.current_week-self.forum_post_week_interval)
            points += self.forum_post_multipler * (stat_data.total_forum_posts - previous_forum_posts)

        # multiplying by None type produces weird results
        # so we do these calculations only if stat_data.score exists
        if stat_data.score:
            points += int(self.anime_score_multipler * stat_data.score)
        return points


    def get_anime_simulcast_region_counts(self, session: Session) -> Dict[int, int]:
        print("Getting region counts of each anime in simulcast file")
        anime_simulcast_region_counts = {}
        if self.simulcast_lines is not None:
            for line in self.simulcast_lines:
                title, subs = line.split("=")
                title = title.strip()
                try:
                    anime = Anime.get_by_name(title, session)
                except sqlalchemy.orm.exc.NoResultFound:
                    print(f"{title} is not found in database")
                    continue

                num_regions = len(
                    [entry for entry in subs.split() if entry == "simul"]
                )
                anime_simulcast_region_counts[anime.mal_id] = num_regions
        return anime_simulcast_region_counts

    def get_licensed_anime(self, session: Session) -> Set[int]:
        print("Getting licensed anime from licenses file")
        licensed_anime = set()
        if self.licenses_lines is not None:
            for title in self.licenses_lines:
                title = title.strip()
                try:
                    anime = Anime.get_by_name(title, session)
                except sqlalchemy.orm.exc.NoResultFound:
                    print(f"{title} is not found in database")
                    continue

                licensed_anime.add(anime.mal_id)
        return licensed_anime

    def _execute(self, session: Session, season: Season) -> None:
        anime_simulcast_region_counts = self.get_anime_simulcast_region_counts(session)
        licensed_anime = self.get_licensed_anime(session)

        anime_list = season.get_all_anime()

        anime_ids_collected = [
            row[0]
            for row in session.query(orm.AnimeWeeklyStat.anime_id)
            .join(orm.Anime)
            .filter(orm.AnimeWeeklyStat.week == self.current_week)
            .filter(orm.Anime.season_id == season._entity.id)
            .all()
        ]

        if anime_ids_collected:
            action = input(
                "At least some anime stats have been collected for this week"
                " already. How should we proceed (overwrite/collect-missing/abort)?"
            )
            if action == "collect-missing":
                anime_list = (
                    anime
                    for anime in anime_list
                    if anime.mal_id not in anime_ids_collected
                )
            elif action == "overwrite":
                pass
            else:
                return

        # for each anime, get the number of teams that have it on active
        anime_active_counts = dict(
            session.query(orm.Anime.id, func.count("*"))
            .join(orm.TeamWeeklyAnime.anime)
            .filter(orm.TeamWeeklyAnime.week == self.current_week)
            .filter(orm.Anime.season_id == season._entity.id)
            .filter(orm.TeamWeeklyAnime.bench == 0)
            .group_by(orm.Anime.id)
            .all()
        )
        double_score_max_num_teams = math.floor(
            self.percent_ownership_for_double_score
            / 100
            * len(list(season.get_all_teams()))
        )

        # casting until update in sqlalchemy-stubs
        for anime in cast(List[Anime], anime_list):
            print(f"Populating stats for {anime}")
            try:
                stat_data = self.get_anime_stats_from_jikan(anime)
            except jikanpy.exceptions.APIException as e:
                print(
                    f"Jikan servers did not handle our request very well, skipping: {e}"
                )
                continue

            if (
                self.is_week_to_calculate("scoring.simulcast")
                and anime.mal_id not in anime_simulcast_region_counts
            ):
                print(
                    f"{anime} doesn't have an entry in simulcast file"
                )

            stat_data.total_points = self.calculate_anime_weekly_points(
                anime,
                stat_data,
                anime_active_counts.get(anime.mal_id, 0),
                double_score_max_num_teams,
                anime_simulcast_region_counts.get(anime.mal_id, 0),
                anime.mal_id in licensed_anime,
            )

            anime_weekly_stat = orm.AnimeWeeklyStat()
            for key, value in attr.asdict(stat_data).items():
                setattr(anime_weekly_stat, key, value)

            session.merge(anime_weekly_stat)
            time.sleep(self.jikan_request_interval)
