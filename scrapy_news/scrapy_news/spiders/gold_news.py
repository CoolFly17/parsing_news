from datetime import datetime
import re
from datetime import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_news.items import NewsItem

class GoldNewsSpider(CrawlSpider):
    name = 'gold_news'
    # Здесь добавляем нужный нам домен и сайт для парсинга
    allowed_domains = ['haaretz.com']
    start_urls = ['https://www.haaretz.com/']

    rules = (
        Rule(
            LinkExtractor(allow_domains=allowed_domains, unique=True),
            callback='parse_item',
            follow=True
        ),
    )
    # Доп фразы
    security_terms = ["цена"]
    gold_pattern = r"золот\w*|gold\w*"
    sec_pattern = r"|".join(re.escape(term) for term in security_terms)
    gold_re = re.compile(rf"\b(?:{gold_pattern}|{sec_pattern})\b", re.IGNORECASE)

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_date = (
            datetime.strptime(start_date, "%Y-%m-%d").date()
            if start_date else None
        )
        self.end_date = (
            datetime.strptime(end_date, "%Y-%m-%d").date()
            if end_date else None
        )

    def parse_item(self, response):
        title = response.css('h1::text').get()
        if not title:
            return

        title = title.strip()
        if not self.gold_re.search(title):
            return

        dt = (
            response.css('time::attr(datetime)').get()
            or response.xpath('//meta[@property="article:published_time"]/@content').get()
        )
        if not dt:
            return

        try:
            pub_date = datetime.fromisoformat(dt[:10]).date()
        except ValueError:
            return

        if self.start_date and pub_date < self.start_date:
            return
        if self.end_date and pub_date > self.end_date:
            return

        yield NewsItem(
            date=pub_date.isoformat(),
            source=response.url.split('/')[2],
            title=title,
            url=response.url
        )
