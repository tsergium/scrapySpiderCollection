# -*- coding: utf-8 -*-
import scrapy
from scrapySpiderCollection.items import TextItem


class JustshowerthoughtsSpider(scrapy.Spider):
    name = "justshowerthoughts"
    allowed_domains = ["justshowerthoughts.com"]
    start_urls = (
        'http://www.justshowerthoughts.com/page/1',
    )

    base_url = 'http://www.justshowerthoughts.com/page/'
    page = 1

    def parse(self, response):
        posts = response.xpath("normalize-space(//div[@class='post-content']/div[@class='body-text']/p/text())").extract()
        for post in posts:
            item = TextItem()
            item['text'] = post
            yield item

        self.page += 1
        if self.page < 142:
            next_page = self.base_url + str(self.page)
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)