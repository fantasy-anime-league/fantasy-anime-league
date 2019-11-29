from sqlalchemy import create_engine, select, exc, event
from sqlalchemy.sql.expression import ColumnElement
import sqlalchemy.orm

from contextlib import contextmanager
from typing import Generator
import sys
import configparser
import urllib

config = configparser.ConfigParser()
config.read("config-secret.ini")

connect_string = (
    f'mysql+pymysql://{config["mfalncfm_main"]["username"]}:'
    f'{urllib.parse.quote_plus(config["mfalncfm_main"]["password"])}@'
    f"127.0.0.1/mfalncfm_main"
)

# TODO: tunneling from here using sshtunnel/paramiko does not work and I can't figure out why!
#      workaround for now is set up the port forwarding manually with PuTTY
#      https://www.namecheap.com/support/knowledgebase/article.aspx/1249/89/how-to-remotely-connect-to-a-mysql-database-located-on-our-shared-server


@contextmanager
def session_scope(echo: bool = False) -> Generator[sqlalchemy.orm.Session, None, None]:
    """Returns a database session to be managed in a with statement

    e.g.
    with session_scope() as session:
        query = session.query(Season).filter(Season.id == 1)
        ...
    """

    engine = create_engine(
        connect_string, echo=echo, echo_pool=echo, pool_pre_ping=True
    )
    session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
    session = session_factory()

    # neither pool_pre_ping nor the legacy recipe on sqlalchemy's website to test connection seems to work so
    # here we do a crude ping on the connection to see if we're successful
    try:
        session.scalar(select([1]))
    except exc.OperationalError as identifier:
        print(
            "Error connecting to MySQL. Did you forget to set up port forwarding? \n"
            "https: // www.namecheap.com/support/knowledgebase/article.aspx/1249/89/how-to-remotely-connect-to-a-mysql-database-located-on-our-shared-server\n"
            f"{identifier}"
        )
        sys.exit(1)

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
