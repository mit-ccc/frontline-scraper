

from scrapy import Spider, Request

from frontline.items import FilmHTMLItem, TranscriptHTMLItem


class FilmSpider(Spider):

    name = 'film'

    start_urls = ['https://www.pbs.org/wgbh/frontline/watch/']

    def parse(self, res):
        """Generate requests for film profiles, walk pagination.
        """
        # Queue films.
        for url in res.css('.all-video a.list__item::attr(href)').extract():
            yield res.follow(url, self.parse_film)

        # Queue next page.
        next_url = (
            res.css("a.pagination__next::attr(href)")
            .extract_first()
        )

        if next_url:
            yield res.follow(next_url)

    def parse_film(self, res):
        """Parse film profile page.
        """
        # Scrape film HTML.
        yield FilmHTMLItem.from_res(res)

        # Queue next page.
        transcript_url = (
            res.css("a.transcript::attr(href)")
            .extract_first()
        )

        if transcript_url:
            yield res.follow(transcript_url, self.parse_transcript)

    def parse_transcript(self, res):
        """Parse film profile page.
        """
        # Scrape film HTML.
        yield TranscriptHTMLItem.from_res(res)
