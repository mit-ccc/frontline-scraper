

import os

from urllib.parse import urlparse

from scrapy.item import Item, Field, ItemMeta

from frontline.models import FilmHTML


class SQLAlchemyItemMeta(ItemMeta):

    def __new__(meta, name, bases, dct):
        """Set item fields from SQLAlchemy columns.
        """
        cls = ItemMeta.__new__(meta, name, bases, dct)

        if cls.model:

            for col in cls.model.__table__.columns:
                cls.fields[col.name] = Field()

        return cls


class SQLAlchemyItem(Item, metaclass=SQLAlchemyItemMeta):

    model = None

    def row(self):
        """Make the SQLAlchemy model instance.
        """
        return self.model(**self)


class FilmHTMLItem(SQLAlchemyItem):

    model = FilmHTML

    @classmethod
    def from_res(cls, res):
        """Parse URL, get HTML.
        """
        url = urlparse(res.url)
        slug = url.path.strip('/').split('/')[-1]

        # TODO: Get title too.
        html = res.css('.page-meta--description').extract_first()

        return cls(slug=slug, html=html)
