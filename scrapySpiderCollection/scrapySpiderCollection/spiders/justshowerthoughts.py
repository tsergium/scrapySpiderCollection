# -*- coding: utf-8 -*-
import scrapy
from scrapySpiderCollection.items import TextItem


class JustshowerthoughtsSpider(scrapy.Spider):
    name = "justshowerthoughts"
    allowed_domains = ["justshowerthoughts.com"]
    start_urls = (
        'http://www.justshowerthoughts.com/page/1',
    )

    def parse(self, response):
        posts = response.xpath("normalize-space(//div[@class='post-content']/div[@class='body-text']/p/text())").extract()
        for post in posts:
            item = TextItem()
            item['content'] = post
            yield item

        next_page = response.xpath("//div[@id='pagination']/a[@class='next']/@href").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)