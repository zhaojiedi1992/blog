# -*- coding: utf-8 -*-
import scrapy
from ..items import *

class BlogSpider(scrapy.Spider):

    name = "blog"
    start_urls=["http://www.cnblogs.com/zhaojiedi1992/default.html?page=1"]
    def parse(self, response):
        lis=response.css(".postTitle a::attr(href)").extract()
        for li in lis:
            next_page=li
            yield scrapy.Request(next_page,callback=self.parse_item)
        next_page=response.css("#nav_next_page a::attr(href)").extract_first()
        if next_page is  not None:
            yield scrapy.Request(next_page, callback=self.parse)
        pages=response.css(".pager a::attr(href)").extract()
        for page in pages:
            yield scrapy.Request(page, callback=self.parse)
    def parse_item(self,response):
        self.logger.info("." *10 +response.url)
        result=BlogItem()
        result["url"]=response.css("#cb_post_title_url::attr(href)").extract_first()
        result["title"]=response.css("#cb_post_title_url::text").extract_first()
        result["date"]=response.css("#post-date::text").extract_first()
        result["read"]=response.css("#post_view_count::text").extract_first()
        result["say"]=response.css("#post_comment_count::text").extract_first()
        yield  result