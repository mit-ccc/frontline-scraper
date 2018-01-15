

from scrapy import Spider, Request


class FilmSpider(Spider):

    name = 'film'

    start_urls = ['https://www.pbs.org/wgbh/frontline/watch/']

    def parse(self, res):
        """Generate requests for film profiles, walk pagination.
        """
        # Scrape films.
        for url in res.css('.all-video a.list__item::attr(href)').extract():
            yield Request(url, self.parse_film)

        # Continue to the next page.

        next_url = (
            res.css("a.pagination__next::attr(href)")
            .extract_first()
        )

        if next_url:
            yield Request(next_url)

    def parse_film(self, res):
        """Parse film profile page.
        """
        desc = res.css('.page-meta--description').extract_first()
        # TODO: item

        # Scrape transcript.

        transcript_url = (
            res.css("a.transcript::attr(href)")
            .extract_first()
        )

        if transcript_url:
            yield Request(transcript_url, self.parse_transcript)

    def parse_transcript(self, res):
        """Parse film profile page.
        """
        print(res)
