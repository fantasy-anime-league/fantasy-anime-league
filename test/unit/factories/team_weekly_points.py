import factory

from .session import session_factory
from .team import TeamFactory
from fal.models import TeamWeeklyPoints

class TeamWeeklyPointsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = TeamWeeklyPoints
        sqlalchemy_session = session_factory

    @factory.lazy_attribute
    def team_id(self):
        return self.team.id

    team =  factory.SubFactory(TeamFactory)
    week = 0
    weekly_points = None
    total_points = None
    is_highest = 0