from pytest_factoryboy import register
import pytest
import factories
import contextlib

register(factories.SeasonFactory)
register(factories.AnimeFactory)
register(factories.TeamFactory)


@pytest.fixture
def session():
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
