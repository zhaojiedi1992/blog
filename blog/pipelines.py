# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BlogPipeline(object):
    def process_item(self, item, spider):
        return item
from scrapy import signals
from scrapy.exporters import *
class BaseExportPipeLine(object):
    def __init__(self,exporter,dst):
        self.files = {}
        self.exporter=exporter
        self.dst=dst
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.dst, 'wb')
        self.files[spider] = file
        self.exporter = self.exporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class JsonExportPipeline(BaseExportPipeLine):
    def __init__(self):
        super(JsonExportPipeline, self).__init__(JsonItemExporter,"items.json")
        #self.exporter["indent"]=2
        #self.exporter["ensure_ascii"]="utf-8"
class JsonLinesExportPipeline(BaseExportPipeLine):
    def __init__(self):
        super(JsonLinesExportPipeline, self).__init__(JsonLinesItemExporter,"items.jl")
        #self.exporter["ensure_ascii"]="utf-8"
class XmlExportPipeline(BaseExportPipeLine):
    def __init__(self):
        super(XmlExportPipeline, self).__init__(XmlItemExporter,"items.xml")
        #self.root_element = 'items'
        #self.item_element = 'item'
        #self.encoding = 'utf-8'
class CsvExportPipeline(BaseExportPipeLine):
    def __init__(self):
        super(CsvExportPipeline, self).__init__(CsvItemExporter,"items.csv")
        #self.encoding = 'utf-8'
        #self.include_headers_line = True
        #self.stream["encoding"]="utf-8"
        #self._join_multivalued=","
class  PickleExportPipeline(BaseExportPipeLine):
    def __init__(self):
        super(PickleExportPipeline, self).__init__(PickleItemExporter,"items.pickle")
class  MarshalExportPipeline(BaseExportPipeLine):
    def __init__(self):
        super(MarshalExportPipeline, self).__init__(MarshalItemExporter,"items.marsha")
class  PprintExportPipeline(BaseExportPipeLine):
    def __init__(self):
        super(PprintExportPipeline, self).__init__(PprintItemExporter,"items.pprint.jl")