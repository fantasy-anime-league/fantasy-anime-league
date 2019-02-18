from fal.models.anime import Anime
from fal.clients.mfalncfm_main import session_scope

import pytest


@pytest.mark.parametrize('id,name,season,alias,sequel', [
    (36432, 'Toaru Majutsu no Index III', 1, None, True),
    (36000, 'Sora to Umi no Aida', 1, 'test alias', False)
])
def test_query_anime(id, name, season, alias, sequel):
    with session_scope(True) as session:
        for row in session.query(Anime).filter(Anime.id == id):
            assert row.name == name
            assert row.season == season
            assert row.alias == alias
            assert row.sequel == sequel
