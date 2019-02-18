from fal.models import Season
from fal.clients.mfalncfm_main import session_scope


def test_retrieve_teams():
    with session_scope(True) as session:
        query = session.query(Season).filter(Season.id == 1)
        season = query.one()
        assert len(season.teams) == 2
        assert sorted(season.teams, key=lambda team: team.id)[
            0].name == 'kei-clone'
