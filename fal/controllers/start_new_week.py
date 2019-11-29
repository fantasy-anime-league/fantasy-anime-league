from sqlalchemy.orm import Session

from fal.models import Season, SeasonOfYear
from .base import Controller


class StartNewWeek(Controller):
    def _execute(self, session: Session, season: Season) -> None:
        season.init_new_week(self.current_week)
