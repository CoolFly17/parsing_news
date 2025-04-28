BOT_NAME = 'scrapy_news'

SPIDER_MODULES = ['scrapy_news.spiders']
NEWSPIDER_MODULE = 'scrapy_news.spiders'

ITEM_PIPELINES = {
    'scrapy_news.pipelines.NewsPipeline': 300,
}

# в этом варианте пайплайн сам пишет CSV, Feeds не нужен
FEED_EXPORT_ENCODING = 'utf-8'
