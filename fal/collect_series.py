from fal.clients.mfalncfm_main import session_scope
from fal.models import Anime, Season


from jikanpy import Jikan
from sqlalchemy.orm import Session

from typing import Dict, ItemsView, ValuesView
import configparser


def get_series(season: str, year: int) -> Dict[int, str]:
    """Retrieve a list of (anime_id, anime_title) from the season info.

    Arguments:
        season: season to get series from
        year: year to get series from

    Returns:
        A dict from anime_id to anime_title. For example:

        {25879: 'Working!!!'}
    """
    jikan = Jikan()
    # Get list of anime in the season
    season_info = jikan.season(year=year, season=season)
    assert season_info["season_name"].lower() == season
    assert season_info["season_year"] == year

    tv_anime = dict()
    for anime in season_info["anime"]:
        if anime["type"] == "TV":
            tv_anime[anime["mal_id"]] = anime["title"]
    return tv_anime


def output_series(series: ItemsView[int, str], filename: str) -> None:
    """Output series ids and titles in the format:

    id_1 title_1
    id_2 title_2
    """
    with open(filename, "w", encoding="utf8") as f:
        f.writelines(f"{a_id} {a_title}\n" for a_id, a_title in sorted(series))


def output_series_titles(titles: ValuesView[str], filename: str) -> None:
    """Output series titles sorted lexicographically in the format:

    title_1
    title_2
    """
    with open(filename, "w", encoding="utf8") as f:
        f.writelines(f"{title}\n" for title in sorted(titles))


def get_season_from_database(season_of_year: str, year: int, session: Session) -> Season:
    """Adds the season to the Season table in the database if necessary, then returns Season object
    """
    query = session.query(Season).filter(
        Season.season_of_year == season_of_year, Season.year == year)
    current_season = query.one_or_none()

    if not current_season:
        new_season = Season(season_of_year=season_of_year, year=year)
        print(f'Adding {new_season} to database')
        session.add(new_season)
        session.commit()
        query = session.query(Season).filter(
            Season.season_of_year == season_of_year, Season.year == year)
        current_season = query.one()

    return current_season


def add_anime_to_database(id: int, name: str, season: Season, session: Session) -> None:
    """ Adds new anime row to database if it doesn't already exist """
    query = session.query(Anime).filter(Anime.id == id)
    anime = query.one_or_none()

    if anime:
        print(f'{anime} already exists in database')
    else:
        anime = Anime(id=id, name=name, season_id=season.id)
        print(f'Adding {anime} to database')
        session.add(anime)


def collect_series() -> None:
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Ensure season is lowercase string and year is integer
    season_of_year = config["season info"]["season"].lower()
    year = int(config["season info"]["year"])

    series_dict = get_series(season_of_year, year)

    # text files workflow
    series = series_dict.items()
    print(len(series))

    output_series(series, "series.txt")
    output_series_titles(series_dict.values(), "series_sorted.txt")

    # database workflow
    print("adding anime to database")
    with session_scope() as session:
        season = get_season_from_database(season_of_year, year, session)
        for anime_id, anime_name in series_dict.items():
            add_anime_to_database(anime_id, anime_name, season, session)
