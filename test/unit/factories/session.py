from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

import fal.models

engine = create_engine('sqlite://')
fal.models.Base.metadata.create_all(engine)
session_factory = scoped_session(sessionmaker(bind=engine))
