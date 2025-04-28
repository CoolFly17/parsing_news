import csv
from pathlib import Path
from datetime import datetime

class NewsPipeline:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        result_dir = Path('results')
        result_dir.mkdir(exist_ok=True)

        date_pref = spider.start_date or datetime.now().strftime('%Y-%m-%d')
        ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        out_file = result_dir / f'news_{date_pref}_{ts}.csv'

        csv.register_dialect(
            'unix',
            delimiter=',',
            lineterminator='\n',
            quoting=csv.QUOTE_MINIMAL
        )

        fieldnames = ['date', 'source', 'title', 'url']
        with out_file.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='unix')
            writer.writeheader()
            writer.writerows(self.items)
