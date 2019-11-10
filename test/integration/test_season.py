from fal.orm import Season
from fal.clients.mfalncfm_main import session_scope


def test_retrieve_teams():
    with session_scope(True) as session:
        query = session.query(Season).filter(Season.id == 1)
        season = query.one()
        assert len(season.teams) == 3

        sorted_teams = sorted(season.teams, key=lambda team: team.id)

        assert sorted_teams[0].name == "kei-clone"
        assert sorted_teams[1].name == "abhinavk99"
        assert sorted_teams[2].name == "Congress"
