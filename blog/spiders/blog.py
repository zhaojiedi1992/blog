# -*- coding: utf-8 -*-
import scrapy
from ..items import *

class BlogSpider(scrapy.Spider):

    name = "blog"

    def __init__(self,user="zhaojiedi1992", *args, **kwargs):
        super(BlogSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.cnblogs.com/%s/default.html?page=1" % user]
        #http://www.cnblogs.com/mvc/blog/ViewCountCommentCout.aspx?postId=7416411
        #http://www.cnblogs.com/mvc/blog/GetComments.aspx?postId=7416411&blogApp=zhaojiedi1992&pageIndex=0&anchorCommentId=0
        self.user=user
        self.Items=[]
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
        #http://i.cnblogs.com/EditPosts.aspx?postid=7416411
        result["postid"]=response.css(".postDesc a[rel]::attr(href)").extract_first()[-7:]
        result["readurl"]=response.css(".postDesc a[rel]::attr(href)").extract_first()
        result["sayurl"] = response.css(".postDesc a[rel]::attr(href)").extract_first()
        self.Items.append(result)
        yield scrapy.Request("http://www.cnblogs.com/mvc/blog/ViewCountCommentCout.aspx?postId=%s" % result["postid"],callback=self.parse_item_read)
        yield scrapy.Request("http://www.cnblogs.com/mvc/blog/GetComments.aspx?postId=%s&blogApp=%s&pageIndex=0&anchorCommentId=0" % result["postid"],self.user ,callback=self.parse_item_say)
    def parse_item_read(self,response):
        readurl=response.url
        elems = [ x for x in self.Items if x["readurl"]==readurl]
        if len(elems)==1:
            elem=elems[0]
            elem["read"]=response.css("body::text").extract_first()
        else:
            pass
    def parse_item_say(self,response):
        readurl=response.url
        elems = [ x for x in self.Items if x["say"]==readurl]
        if len(elems)==1:
            elem=elems[0]
            elem["read"]=response.css("body::text").extract_first()
        else:
            pass


