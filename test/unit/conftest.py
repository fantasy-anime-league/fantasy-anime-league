import contextlib

from pytest_factoryboy import register
import pytest
import factories
import sqlalchemy

import fal.models

register(factories.SeasonFactory)
register(factories.AnimeFactory)
register(factories.TeamFactory)
register(factories.TeamWeeklyAnimeFactory)


@pytest.fixture
def session():
    engine = sqlalchemy.create_engine('sqlite://')
    fal.models.Base.metadata.create_all(engine)
    factories.session_factory.configure(bind=engine)

    _session = factories.session_factory()
    yield _session
    _session.rollback()
    factories.session_factory.remove()


@pytest.fixture
def session_scope():
    _session = factories.session_factory()

    @contextlib.contextmanager
    def _session_scope():
        yield _session

    yield _session_scope
    _session.rollback()
    factories.session_factory.remove()
