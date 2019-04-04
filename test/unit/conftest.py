import contextlib
from typing import Iterable, Mapping

from pytest_factoryboy import register
import pytest
import factories
import sqlalchemy

import fal.models

register(factories.SeasonFactory)
register(factories.AnimeFactory)
register(factories.TeamFactory)
register(factories.TeamWeeklyAnimeFactory)


@pytest.fixture()
def session_factory():
    engine = sqlalchemy.create_engine('sqlite://', echo=True)
    fal.models.Base.metadata.create_all(engine)
    factories.session_factory.configure(bind=engine)
    return factories.session_factory


@pytest.fixture
def session(session_factory):
    _session = session_factory()
    yield _session
    _session.rollback()
    session_factory.remove()


@pytest.fixture
def session_scope(session_factory):
    _session = session_factory()

    @contextlib.contextmanager
    def _session_scope():
        yield _session

    yield _session_scope
    _session.rollback()
    session_factory.remove()


class Config(object):
    def __init__(
        self,
        sections: Iterable[str],
        kv: Mapping
    ):
        self.sections = sections
        self.kv = kv

    def __call__(self, section, key):
        assert section in self.sections
        if key in self.kv:
            return self.kv[key]
        raise KeyError(f'Unexpected key {key} passed into config')


@pytest.fixture(scope='session')
def config_functor():
    def _config_functor(sections, kv):
        return Config(sections, kv)
    return _config_functor
