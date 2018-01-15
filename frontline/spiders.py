

from scrapy import Spider, Request


class FilmSpider(Spider):

    name = 'film'

    start_urls = ['https://www.pbs.org/wgbh/frontline/watch/']

    def parse(self, res):
        """TODO
        """
        print(res)

        # Continue to the next page.

        next_url = (
            res.xpath("//a[contains(@class, 'pagination__next')]/@href")
            .extract_first()
        )

        if next_url:
            yield Request(next_url)
