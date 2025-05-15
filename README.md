# parsing_news - сервис, позволяющий парсить новостные заголовки СМИ


## Как запустить

1. Клонировать репозиторий и перейти в папку проекта:

```bash
   git clone <git@github.com:CoolFly17/parsing_news.git>
```

2. Создать и активировать виртуальное окружение:

```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
```

3. Установить зависимости:

```bash
   pip install -r requirements.txt
```

4. Запустить приложение (указываем дату начала и конца):

```bash
   scrapy crawl gold_news -a start_date=2022-01-01 -a end_date=2022-12-31
```

5. Результаты:

Результаты будут храниться в csv файле в папке results

