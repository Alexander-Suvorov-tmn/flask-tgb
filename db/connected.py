import os
from os import path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


ROOT = path.dirname(path.realpath(__file__))
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/tgbot')
# os.environ.get('DATABASE_URL')
sess = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()
Base.query = sess.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
