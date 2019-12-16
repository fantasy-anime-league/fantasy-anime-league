import configparser
import abc

from sqlalchemy.orm import Session

import attr
import jikanpy

from fal.orm.mfalncfm_main import session_scope
from fal.models import SeasonOfYear, Season

config = configparser.ConfigParser()
config.read("config.ini")


@attr.s(auto_attribs=True, kw_only=True)
class Controller(abc.ABC):
    """
    Ideally, controllers should take care of configuration when the class initializes
    so that the business logic doesn't have to worry about it.
    """

    current_week: int = config.getint("weekly info", "current-week")
    season_of_year: SeasonOfYear = SeasonOfYear(
        config.get("season info", "season").lower()
    )
    year: int = config.getint("season info", "year")

    jikan: jikanpy.Jikan = attr.Factory(jikanpy.Jikan)
    jikan_request_interval: int = config.getint("jikanpy", "request-interval")

    def execute(self) -> None:
        with session_scope() as session:
            season = Season.get_or_create(
                season_of_year=self.season_of_year, year=self.year, session=session,
            )
            self._execute(session, season)

    @abc.abstractmethod
    def _execute(self, session: Session, season: Season) -> None:
        """
        Every controller currently uses a session and a season.
        Might as well provide it up front.
        """
        pass
