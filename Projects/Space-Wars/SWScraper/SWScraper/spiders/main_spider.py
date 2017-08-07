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
        i = 0
        for href in response.xpath(
                '//div[@class="fusion-column-wrapper"]/p/a/@href'
        ).extract():
            # For each festival link, call 'parse_ST' (defined later)
            if i < 10:
                series = 'Motion Picture'
                start = 'various'
                end = 'various'
            elif 10 <= i < 186:
                series = 'The Next Generation'
                start = 1987
                end = 1994
            elif 186 <= i < 359:
                series = 'Deep Space 9'
                start = 1993
                end = 1999
            elif 359 <= i < 530:
                series = 'Voyager'
                start = 1995
                end = 2001
            elif 530 <= i < 627:
                series = 'Enterprise'
                start = 2001
                end = 2005
            else:
                series = 'The Original Series'
                start = 1966
                end = 1969

            yield scrapy.Request(
                url=href,
                callback=self.parse_ST,
                meta={
                'url':href,
                'series': series,
                'start': start,
                'end': end
                }
            )
            i +=1

    def parse_ST(self, response):
            url = response.request.meta['url']
            series = meta['series']
            start = meta['start']
            end = meta['end']
            raw_text = response.xpath('//text()').extract()

            yield {
                'url': url,
                'series': series,
                'start': start,
                'end': end,
                'raw_text': raw_text
            }
