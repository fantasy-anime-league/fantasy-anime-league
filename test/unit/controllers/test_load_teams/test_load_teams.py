from unittest.mock import patch
import pytest
import factory

from fal.controllers import load_teams
from fal.orm import TeamWeeklyAnime, Team


@patch("fal.controllers.load_teams.config")
@pytest.mark.parametrize(
    "team_input, teamname, active, bench",
    [
        pytest.param(
            [
                "Team: kei-clone",
                "Toaru Majutsu no Index III",
                "Zombieland Saga",
                "Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo Minai",
                "Kishuku Gakkou no Juliet",
                "Radiant",
                "RErideD: Tokigoe no Derrida",
                "Ore ga Suki nano wa Imouto dakedo Imouto ja Nai",
            ],
            "kei-clone",
            [
                "Toaru Majutsu no Index III",
                "Zombieland Saga",
                "Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo Minai",
                "Kishuku Gakkou no Juliet",
                "Radiant",
            ],
            [
                "RErideD: Tokigoe no Derrida",
                "Ore ga Suki nano wa Imouto dakedo Imouto ja Nai",
            ],
            id="normal",
        )
    ],
)
def test_slice_up_team_input(config_mock, team_input, teamname, active, bench):
    def mock_config(section, key):
        assert section == "season info"
        if key == "num-active-on-team":
            return 5
        if key == "num-on-bench":
            return 2
        raise KeyError

    config_mock.getint.side_effect = mock_config
    team_lines = load_teams.slice_up_team_input(team_input)
    config_mock.getint.assert_called()
    assert team_lines.teamname == teamname
    assert team_lines.active == active
    assert team_lines.bench == bench


@patch("fal.controllers.load_teams.config")
@pytest.mark.parametrize(
    "team_input",
    [
        pytest.param(
            [
                "Team: kei-clone",
                "Toaru Majutsu no Index III",
                "Zombieland Saga",
                "Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo Minai",
                "Kishuku Gakkou no Juliet",
                "Radiant",
                "RErideD: Tokigoe no Derrida",
                "Ore ga Suki nano wa Imouto dakedo Imouto ja Nai",
            ],
            id="too few",
        ),
        pytest.param(
            [
                "Team: kei-clone",
                "Toaru Majutsu no Index III",
                "Zombieland Saga",
                "Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo Minai",
                "Kishuku Gakkou no Juliet",
                "Radiant",
                "RErideD: Tokigoe no Derrida",
                "Ore ga Suki nano wa Imouto dakedo Imouto ja Nai",
                "Suzumiya Haruhi no Yuutsu",
                "Kanon (2006)",
                "Fruits Basket (2019)",
            ],
            id="too many",
        ),
    ],
)
def test_slice_up_team_input_raises_if_length_is_not_expected(config_mock, team_input):
    def mock_config(section, key):
        assert section == "season info"
        if key == "num-active-on-team":
            return 6
        if key == "num-on-bench":
            return 3
        raise KeyError

    config_mock.getint.side_effect = mock_config
    with pytest.raises(AssertionError):
        load_teams.slice_up_team_input(team_input)


def test_add_anime_to_team(session, orm_team_factory, orm_anime_factory):
    team = orm_team_factory()

    active_anime = ["Toaru Majutsu no Index III", "Zombieland Saga"]
    bench_anime = ["Kanon (2006)", "Fruits Basket (2019)"]

    for anime_name in active_anime + bench_anime:
        orm_anime_factory(name=anime_name, eligible=1)

    load_teams.add_anime_to_team(team, active_anime, 0, session)
    load_teams.add_anime_to_team(team, bench_anime, 1, session)

    team_active_anime = (
        session.query(TeamWeeklyAnime)
        .filter(TeamWeeklyAnime.team_id == team.id, TeamWeeklyAnime.bench == 0)
        .all()
    )
    team_bench_anime = (
        session.query(TeamWeeklyAnime)
        .filter(TeamWeeklyAnime.team_id == team.id, TeamWeeklyAnime.bench == 1)
        .all()
    )

    assert len(team_active_anime) == 2
    assert len(team_bench_anime) == 2

    for anime in [x.anime for x in team_active_anime]:
        assert anime.name in active_anime
    for anime in [x.anime for x in team_bench_anime]:
        assert anime.name in bench_anime


@patch("fal.controllers.load_teams.config")
@patch("fal.controllers.load_teams.session_scope")
def test_load_teams(
    session_scope_mock,
    config_mock,
    config_functor,
    shared_datadir,
    session_scope,
    session,
    orm_anime_factory,
    orm_season_factory,
):
    season = orm_season_factory(id=0)

    def mock_config_getitem(key):
        assert key == "season info"
        return {"season": season.season_of_year}

    config_function = config_functor(
        sections=["season info", "weekly info"],
        kv={
            "num-active-on-team": 5,
            "num-on-bench": 2,
            "year": season.year,
            "current-week": 0,
        },
    )

    config_mock.__getitem__.side_effect = mock_config_getitem
    config_mock.getint.side_effect = config_function

    session_scope_mock.side_effect = session_scope

    with (shared_datadir / "anime.txt").open() as f:
        all_anime = f.readlines()
    for anime_name in all_anime:
        orm_anime_factory(name=anime_name.strip(), eligible=1)

    with (shared_datadir / "registration.txt").open() as f:
        registration_data = f.readlines()

    load_teams.load_teams(registration_data)

    teams = session.query(Team).all()
    assert len(teams) == 3

    for team in teams:
        team_active_anime = (
            session.query(TeamWeeklyAnime)
            .filter(TeamWeeklyAnime.team_id == team.id, TeamWeeklyAnime.bench == 0)
            .all()
        )
        team_bench_anime = (
            session.query(TeamWeeklyAnime)
            .filter(TeamWeeklyAnime.team_id == team.id, TeamWeeklyAnime.bench == 1)
            .all()
        )

        assert len(team_active_anime) == 5
        assert len(team_bench_anime) == 2
