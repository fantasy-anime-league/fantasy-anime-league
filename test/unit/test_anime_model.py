from unittest.mock import MagicMock

from fal.models import Anime, Season


def test_add_anime_to_database():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.one_or_none.return_value = None

    expected_anime = Anime(id=1234,
                           name="The Melancholy of Haruhi Suzumiya", season_id=0)

    Anime.add_anime_to_database(
        expected_anime.id, expected_anime.name, Season(id=expected_anime.season_id), mock_session)
    args, _ = mock_session.add.call_args
    anime_added = args[0]
    assert isinstance(anime_added, Anime)
    assert anime_added.id == expected_anime.id
    assert anime_added.name == expected_anime.name
    assert anime_added.season_id == expected_anime.season_id
