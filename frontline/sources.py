

import iso8601
import attr
import ujson

from boltons.iterutils import chunked_iter
from tqdm import tqdm

from .utils import try_or_none
from .db import session
from .models import Tweet


@attr.s
class GnipJSONFile:

    path = attr.ib()

    def tweets(self):
        """Parse lines.
        """
        with open(self.path) as fh:
            for line in fh:
                yield ujson.loads(line.strip())

    def posts(self):
        """Generate "post" tweets.
        """
        for tweet in self.tweets():
            if tweet['verb'] == 'post':
                yield tweet

    def db_mappings(self):
        """Generate Tweet mappings.
        """
        ids = set()

        # TODO: Handle RTs, etc.
        for i, post in enumerate(self.posts()):

            # TODO: Handle in db?
            if post['id'] not in ids:
                yield GnipTweet(post).db_mapping()
                ids.add(post['id'])

    def load(self, n=10000):
        """Bulk-insert database rows.
        """
        pages = chunked_iter(self.db_mappings(), n)

        for mappings in tqdm(pages):

            session.bulk_insert_mappings(Tweet, mappings)
            session.flush()

        session.commit()


class GnipTweet(dict):

    def id(self):
        return self['id']

    def body(self):
        return self['body']

    def posted_time(self):
        return iso8601.parse_date(self['postedTime'])

    def actor_id(self):
        return self['actor']['id']

    def actor_display_name(self):
        return self['actor']['displayName']

    def actor_summary(self):
        return self['actor']['summary']

    def actor_preferred_username(self):
        return self['actor']['preferredUsername']

    def actor_language(self):
        return self['actor']['languages'][0]

    @try_or_none
    def actor_location(self):
        return self['actor']['location']['displayName']

    @try_or_none
    def location_display_name(self):
        return self['location']['displayName']

    @try_or_none
    def location_name(self):
        return self['location']['name']

    @try_or_none
    def location_country_code(self):
        return self['location']['countryCode']

    @try_or_none
    def location_twitter_country_code(self):
        return self['location']['twitterCountryCode']

    @try_or_none
    def location_twitter_place_type(self):
        return self['location']['twitterPlaceType']

    @try_or_none
    def geo_lat(self):
        return float(self['geo']['coordinates'][0])

    @try_or_none
    def geo_lon(self):
        return float(self['geo']['coordinates'][1])

    def db_mapping(self):
        return {col: getattr(self, col)() for col in Tweet.columns()}
