# Some tips for testing

* If your test makes use of any `SQLAlchemyModelFactory` fixture, it will attempt to create a scoped_session using `factories.session.session_factory`. What this means is you need to **make sure that `session` is included as a dependency** in tests that make use of sessions, whether explicitly or implicitly. This will allow the session fixture to set up the sqlite engine correctly.

* To turn on verbosity of sqlalchemy, set `echo=True` in `conftest.py` where we call `sqlalchemy.create_engine`