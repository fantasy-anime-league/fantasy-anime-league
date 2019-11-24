import pytest

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from fal.models import Anime, Season, SeasonOfYear


def test_create_and_retrieve_anime_by_name_and_alias(session):
    season = Season.get_or_create(SeasonOfYear.SPRING, 2006, session)
    anime = Anime.create(1234, "The Melancholy of Haruhi Suzumiya", season, session)

    assert anime == Anime.get_by_name("The Melancholy of Haruhi Suzumiya", session)

    anime.add_alias("Suzumiya Haruhi no Yuutsu")

    assert anime == Anime.get_by_name("Suzumiya Haruhi no Yuutsu", session)


def test_retrieve_anime_does_not_exist(session):
    season = Season.get_or_create(SeasonOfYear.SPRING, 2006, session)
    Anime.create(1234, "The Melancholy of Haruhi Suzumiya", season, session)

    with pytest.raises(NoResultFound):
        Anime.get_by_name("Suzumiya Haruhi no Yuutsu", session)


def test_create_anime_twice_throws_exception(session):
    season = Season.get_or_create(SeasonOfYear.SPRING, 2006, session)
    Anime.create(1234, "The Melancholy of Haruhi Suzumiya", season, session)
    with pytest.raises(IntegrityError):
        Anime.create(1234, "Suzumiya Haruhi no Yuutsu", season, session)
