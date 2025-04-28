import scrapy

class NewsItem(scrapy.Item):
    date = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
