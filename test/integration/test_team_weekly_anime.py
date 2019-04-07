from fal.models import TeamWeeklyAnime
from fal.clients.mfalncfm_main import session_scope

import pytest


@pytest.mark.parametrize('team_id,anime_ids,name,bench_indices', [
    (1, (36000, 36945, 37232, 37555, 37584, 37657, 37992), 'kei-clone', (0, 4)),
    (2, (35847, 36000, 37202, 37430, 37450, 37965, 37991), 'abhinavk99', (0, 2))
])
def test_query_team_weekly_anime(team_id, anime_ids, name, bench_indices):
    with session_scope() as session:
        anime_list = session.query(TeamWeeklyAnime). \
            order_by(TeamWeeklyAnime.anime_id). \
            filter(TeamWeeklyAnime.team_id == team_id). \
            all()
        for i, anime in enumerate(anime_list):
            if i in bench_indices:
                # anime.bench == b'\x01', so we use ord() to convert it to int
                assert ord(anime.bench) == 1
            assert anime.team.name == name
            assert anime.anime_id == anime_ids[i]
