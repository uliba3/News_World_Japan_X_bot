# https://docs.python.org/3/library/json.html
# This library will be used to parse the JSON data returned by the API.
import json
import os
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request
# This library will be used to fetch the API.
import urllib.request
import datetime
from dotenv import load_dotenv
import time

load_dotenv()
NEWS_API_ORG_API_KEY = os.getenv("NEWS_API_ORG_API_KEY")
base_url = "https://gnews.io/api/v4/"
categories = ["general", "world", "business"]
# ["general", "world", "nation", "business", "technology", "entertainment", "sports", "science", "health"]
def add_all_articles(url, language):
    articles = []
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        all_articles = data["articles"]
    for article in all_articles:
        date = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()
        articles.append({
            "title": article['title'],
            "url": article['url'],
            "date": date,
            "language": language
        })
    return articles

def remove_duplicate_articles(articles):
    seen_titles = set()
    for article in articles:
        if article['title'] in seen_titles:
            articles.remove(article)
        else:
            seen_titles.add(article['title'])
    print(articles)
    return articles

def add_english_articles():
    articles = []
    for category in categories:
        time.sleep(1)
        category_url = f"{base_url}top-headlines?topic={category}&lang=en&apikey={NEWS_API_ORG_API_KEY}"
        articles += add_all_articles(category_url, "en")
    return remove_duplicate_articles(articles)

def add_japanese_articles():
    articles = []
    for category in categories:
        time.sleep(1)
        category_url = f"{base_url}top-headlines?topic={category}&lang=ja&apikey={NEWS_API_ORG_API_KEY}"
        articles += add_all_articles(category_url, "ja")
    return remove_duplicate_articles( articles )

if __name__ == '__main__':
    #add_japanese_articles()
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    print(today_utc)