from fal.models import Anime
from fal.clients.mfalncfm_main import session_scope

import pytest


@pytest.mark.parametrize('id,name,season_id,alias,sequel,season_of_year,year', [
    (36432, 'Toaru Majutsu no Index III', 1, None, True, None, "fall", 2018),
    (36000, 'Sora to Umi no Aida', 1, 'test alias', False, None, "fall", 2018)
])
def test_query_anime(id, name, season_id, alias, sequel, eligible, season_of_year, year):
    with session_scope(True) as session:
        query = session.query(Anime).filter(Anime.id == id)
        anime = query.one()
        assert anime.name == name
        assert anime.season_id == season_id
        assert anime.alias == alias
        assert anime.sequel == sequel
        assert anime.eligible == eligible

        assert anime.season.season_of_year == season_of_year
        assert anime.season.year == year
