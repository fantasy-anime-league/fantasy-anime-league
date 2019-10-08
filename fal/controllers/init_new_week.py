from __future__ import annotations

import configparser

from fal.clients.mfalncfm_main import session_scope
from fal.models import TeamWeeklyAnime, Season, Team

config = configparser.ConfigParser()
config.read("config.ini")

def init_new_team_weekly_anime() -> None:
    '''Initializes this week with a new set of TeamWeeklyAnime,
    which is the first thing needed before doing other stuff with the week.

    Should fail in theory if you forget to change the week number in config.ini, since
    session.add() shouldn't clobber existing data'''

    season_of_year = config.get("season info", "season").lower()
    year = config.getint("season info", "year")
    week = config.getint("weekly info", "current-week")

    with session_scope() as session:
        season = Season.get_season_from_database(season_of_year, year, session)

        last_week_team_weekly_anime = session.query(TeamWeeklyAnime, Team).filter(
            TeamWeeklyAnime.week == week - 1,
            Team.season_id == season.id,
            Team.id == TeamWeeklyAnime.team_id
        ).all()

        for team_weekly_anime, team in last_week_team_weekly_anime:
            new_team_weekly_anime = TeamWeeklyAnime(
                team_id=team.id,
                anime_id=team_weekly_anime.anime_id,
                week=week,
                bench=team_weekly_anime.bench
            )
            session.add(new_team_weekly_anime)