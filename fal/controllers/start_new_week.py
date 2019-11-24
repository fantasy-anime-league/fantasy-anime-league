from __future__ import annotations

import configparser

from fal.orm.mfalncfm_main import session_scope
from fal.models import Season, SeasonOfYear

config = configparser.ConfigParser()
config.read("config.ini")


def start_new_week() -> None:
    season_of_year = config.get("season info", "season").lower()
    year = config.getint("season info", "year")

    with session_scope() as session:
        season = Season.get_or_create(
            season_of_year=SeasonOfYear(season_of_year.lower()),
            year=year,
            session=session,
        )
        season.init_new_week()
