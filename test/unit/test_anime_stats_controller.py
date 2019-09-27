from unittest.mock import patch
import configparser
import pytest
import vcr
import factory

from fal.controllers import anime_stats
from fal.models import AnimeWeeklyStat, Anime, Season

config = configparser.ConfigParser()
config.read("config.ini")


vcrpath = config.get('vcr', 'path')


@patch('fal.controllers.anime_stats.get_forum_posts')
@patch('fal.controllers.anime_stats.config')
@patch('fal.controllers.anime_stats.session_scope')
@vcr.use_cassette(f"{vcrpath}/anime_stats/populate_anime_weekly_stats.yaml")
def test_populate_anime_weekly_stats(session_scope_mock, config_mock, get_forum_posts, session_scope, config_functor, season_factory, anime_factory):
    '''Currently only testing for week 4 to test dropped scores.
        Feel free to parametrize this test to do other weeks as well
        if we need to test for other scoring configs'''

    session_scope_mock.side_effect = session_scope
    config_function = config_functor(
        sections=[
            'season info',
            'weekly info',
            'jikanpy',
            'scoring info',
            'scoring.dropped',
        ],
        kv={
            'season': 'spring',
            'year': 2018,
            'current-week': 4,
            'forum-posts-every-n-weeks': 2,
            'forum-post-multiplier': 25,
            'request-interval': 0,
            '4': -4  # for 'scoring.dropped' only. others are not valid this week 4
        }
    )
    config_mock.getint.side_effect = config_function
    config_mock.get.side_effect = config_function

    get_forum_posts.return_value = 0

    season_factory(id=0, season_of_year='spring', year=2018)
    anime_factory(id=1, name="Cowboy Bebop")
    anime_factory(id=849, name="Suzumiya Haruhi no Yuuutsu")
    anime_factory(id=30276, name="One Punch Man")

    anime_stats.populate_anime_weekly_stats()
    with session_scope() as session:
        stats = session.query(AnimeWeeklyStat) \
            .order_by(AnimeWeeklyStat.anime_id).all()

    assert len(stats) == 3

    print(stats)
    assert stats[0].watching == 71944
    assert stats[0].completed == 526969
    assert stats[0].anime_id == 1

    assert stats[1].score == 7.96
    assert stats[1].favorites == 14683
    assert stats[1].anime_id == 849

    assert stats[2].dropped == 17066
    assert stats[2].forum_posts == 0
    assert stats[2].anime_id == 30276


@patch('fal.controllers.anime_stats.config')
@vcr.use_cassette(f"{vcrpath}/anime_stats/get_forum_posts.yaml")
def test_get_forum_posts(config_mock, anime_factory, config_functor, session):
    config_mock.getint.side_effect = config_functor(
        sections=['weekly info', 'scoring info'],
        kv={
            'current-week': 6,
            'forum-posts-every-n-weeks': 2,
        }
    )
    one_punch_man = anime_factory(id=30276, name="One Punch Man")
    assert anime_stats.get_forum_posts(one_punch_man) == 327 + 426
