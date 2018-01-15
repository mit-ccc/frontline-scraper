

import re

from datetime import datetime as dt
from dateutil.parser import parse as dt_parse
from cached_property import cached_property
from tqdm import tqdm

from sqlalchemy import Column, DateTime, Date, String, Integer
from sqlalchemy.ext.declarative import declarative_base

from scrapy import Selector

from frontline.utils import try_or_none
from frontline.db import session


Base = declarative_base()
Base.query = session.query_property()


class ScrapyItem:

    url = Column(String, nullable=False)

    scraped_at = Column(DateTime, default=dt.utcnow, nullable=False)


class FilmHTML(Base, ScrapyItem):

    __tablename__ = 'film_html'

    slug = Column(String, primary_key=True)

    html = Column(String, nullable=False)

    @cached_property
    def selector(self):
        return Selector(text=self.html)

    @cached_property
    def title(self):
        """Episode title.
        """
        return (
            self.selector
            .css('.film__tray-title::text')
            .extract_first()
            .strip()
        )

    @cached_property
    def pub_date(self):
        """Parse the publication date.
        """
        raw = (
            self.selector
            .css('.fea--film__pubdate::text')
            .extract_first()
        )

        return dt_parse(raw).date()

    @cached_property
    @try_or_none
    def season_episode(self):
        """Parse season / episode ints.
        """
        text = (
            self.selector
            .css('#film-season-episode::text')
            .extract_first()
        )

        return list(map(int, re.findall('[0-9]+', text)))

    @cached_property
    @try_or_none
    def season(self):
        return self.season_episode[0]

    @cached_property
    @try_or_none
    def episode(self):
        return self.season_episode[1]

    @cached_property
    def description(self):
        """Description blurb.
        """
        ps = (
            self.selector
            .css('.page-meta--description p::text')
            .extract()
        )

        return ps[0]

    def parse(self):
        """Metadata row.
        """
        return Film(
            slug=self.slug,
            title=self.title,
            pub_date=self.pub_date,
            season=self.season,
            episode=self.episode,
            description=self.description,
        )


class Film(Base):

    __tablename__ = 'film'

    slug = Column(String, primary_key=True)

    url = Column(String)

    title = Column(String)

    pub_date = Column(Date)

    season = Column(Integer)

    episode = Column(Integer)

    description = Column(String)

    @classmethod
    def load(cls):
        """Parse rows from HTML.
        """
        for html in tqdm(FilmHTML.query.all()):
            session.add(html.parse())

        session.commit()


class TranscriptHTML(Base, ScrapyItem):

    __tablename__ = 'transcript_html'

    slug = Column(String, primary_key=True)

    html = Column(String, nullable=False)
