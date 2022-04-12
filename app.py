from flask import Flask, render_template
from flask_caching import Cache
import requests
import datetime

config = {
    "DEBUG": True,          # some Flask specific configs
    "USE_RELOADER": True,
    "CACHE_TYPE": "FileSystemCache",  # Flask-Caching related configs
    "CACHE_DIR": "cache",
    "CACHE_DEFAULT_TIMEOUT": 43200 # 12 hours
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


today = datetime.datetime.now()
date = today.strftime('%m/%d')
date_uk = today.strftime('%d/%m')

@cache.cached(key_prefix='items')
def get_items(date):
    url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/' + date
    items = requests.get(url).json()
    return items


@app.route('/')
def homepage():

    # if items is not None:
    #     items = get_items(date)
    #     cache.set("items", items)
    # items = cache.get("items")

    items = get_items(date)
    return render_template('index.html', items=items, date=date_uk)

if __name__ == '__main__':
    app.run()