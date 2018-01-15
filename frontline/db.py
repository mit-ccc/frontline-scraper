

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL


db_path = os.path.join(os.path.dirname(__file__), 'frontline.db')

url = URL(drivername='sqlite', database=db_path)

engine = create_engine(url)

factory = sessionmaker(bind=engine)

session = scoped_session(factory)
