from fal.orm import Anime
from fal.orm.mfalncfm_main import session_scope

import pytest


@pytest.mark.parametrize(
    "id,name,season_id,alias,restricted,eligible,season_of_year,year",
    [
        (36432, "Toaru Majutsu no Index III", 1, None, True, 1, "fall", 2018),
        (36000, "Sora to Umi no Aida", 1, "test alias", False, 1, "fall", 2018),
    ],
)
def test_query_anime(
    id, name, season_id, alias, restricted, eligible, season_of_year, year
):
    with session_scope(True) as session:
        query = session.query(Anime).filter(Anime.id == id)
        anime = query.one()
        assert anime.name == name
        assert anime.season_id == season_id
        assert anime.alias == alias
        assert anime.restricted == restricted
        assert anime.eligible == eligible

        assert anime.season.season_of_year == season_of_year
        assert anime.season.year == year
