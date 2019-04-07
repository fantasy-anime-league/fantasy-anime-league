import contextlib
from typing import Iterable, Mapping


import pytest
import factories
import sqlalchemy
from pytest_factoryboy import register

import fal.models

register(factories.SeasonFactory)
register(factories.AnimeFactory)
register(factories.TeamFactory)
register(factories.TeamWeeklyAnimeFactory)


@pytest.fixture(scope="session")
def transaction():
    engine = sqlalchemy.create_engine('sqlite://', echo=True)
    fal.models.Base.metadata.create_all(engine)
    connection = engine.connect()
    transaction = connection.begin()
    factories.session_factory.configure(bind=connection)
    return transaction

@pytest.fixture
def session(transaction):    
    _session = factories.session_factory()

    yield _session

    _session.close()
    transaction.rollback()


@pytest.fixture
def session_scope(session):
    @contextlib.contextmanager
    def _session_scope():
        yield session

    yield _session_scope


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
