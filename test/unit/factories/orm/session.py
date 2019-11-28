from sqlalchemy.orm import scoped_session, sessionmaker

session_factory = scoped_session(sessionmaker())
