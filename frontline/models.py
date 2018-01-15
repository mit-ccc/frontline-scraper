

from datetime import datetime as dt

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

from frontline.db import session


Base = declarative_base()
Base.query = session.query_property()


class ScrapyItem:
    scraped_at = Column(DateTime, default=dt.utcnow, nullable=False)


class FilmHTML(Base, ScrapyItem):

    __tablename__ = 'film_html'

    slug = Column(String, primary_key=True)

    html = Column(String, nullable=False)
