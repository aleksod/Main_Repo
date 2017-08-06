import scrapy


class StarTrekSpider(scrapy.Spider):
    name = 'star_trek'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCASHE_ENABLED": True
    }

    start_urls = [
    'https://scifi.media/star-trek/transcripts/'
    ]

    def parse(self, response):
        # Extract the links to the individual festival pages
        for href in response.xpath(
                '//div[@class="fusion-column-wrapper"]/p/a/@href'
        ).extract()[10:]:
            # For each festival link, call 'parse_ST' (defined later)
            yield scrapy.Request(
                url=href,
                callback=self.parse_ST,
                meta={'url':href}
            )

    def parse_ST(self, response):
            url = response.request.meta['url']

            raw_text = response.xpath('//text()').extract()

            yield {
                'url': url,
                'raw_text': raw_text
            }
