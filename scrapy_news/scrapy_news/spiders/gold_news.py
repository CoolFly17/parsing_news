import re
from datetime import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_news.items import NewsItem

class GoldNewsSpider(CrawlSpider):
    name = 'gold_news'
    allowed_domains = [
        'rbc.ru',
        'gazeta.ru',
        'news.ru',
        'russian.rt.com',
        'life.ru',
    ]
    start_urls = [
        'https://www.rbc.ru/',
        'https://www.gazeta.ru/',
        'https://news.ru/',
        'https://russian.rt.com/',
        'https://life.ru/',
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=allowed_domains,
                unique=True
            ),
            callback='parse_item',
            follow=True
        ),
    )
    security_terms = [
        "система видеонаблюдения",
        "видеонаблюдение",
        "охранная сигнализация",
        "сигнализация",
        "контроль доступа",
        "биометрический контроль",
        "турникет",
        "электронный замок",
        "датчики движения",
        "газоанализатор",
        "периметр",
        "ограждение периметра",
        "сторожевой пост",
        "охранный пост",
        "патруль",
        "часовой",
        "охранная группа",
        "частное охранное предприятие",
        "КПП",
        "пропускной режим",
        "радиоэлектронные помехи",
        "GPS-мониторинг",
        "RFID-метка",
        "трекер",
        "GPS-трекер",
        "датчик открытия",
        "датчик вскрытия",
        "охранная робототехника",
        "служебная собака",
        "кинологическая служба",
        "противопожарная система",
        "СОУЭ",
        "СОТС"
    ]
    gold_pattern = r"золот\w*|gold\w*"
    sec_pattern = r"|".join(re.escape(term) for term in security_terms)
    gold_re = re.compile(rf"\b(?:{gold_pattern}|{sec_pattern})\b", re.IGNORECASE)

    def __init__(self, start_date=None, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.start_date = start_date

    def parse_item(self, response):
        title = response.css('h1::text').get()
        if not title:
            return

        title = title.strip()
        if not self.gold_re.search(title):
            return

        dt = (
            response.css('time::attr(datetime)').get()
            or response.xpath(
                '//meta[@property="article:published_time"]/@content'
            ).get()
        )
        if not dt:
            return
        pub_date = dt[:10]

        if self.start_date and pub_date < self.start_date:
            return

        source = response.url.split('/')[2]
        url = response.url

        yield NewsItem(date=pub_date, source=source, title=title, url=url)
