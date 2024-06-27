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
categories = ["general", "world", "nation", "business"]

def add_all_articles(url):
    articles = []
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        all_articles = data["articles"]
    for article in all_articles:
        date = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()
        articles.append({
            "title": article['title'],
            "url": article['url'],
            "date": date
        })
    return articles

def add_headline_articles(url):
    articles = []
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        all_articles = data["articles"]
    for article in all_articles:
        date = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()
        articles.append({
            "title": article['title'],
            "url": article['url'],
            "date": date
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
    all_articles_url = f"{base_url}search?q=japan&lang=en&apikey={NEWS_API_ORG_API_KEY}"
    headline_articles_url = f"{base_url}top-headlines?q=japan&lang=en&apikey={NEWS_API_ORG_API_KEY}"
    return remove_duplicate_articles(add_all_articles(all_articles_url) + add_headline_articles(headline_articles_url))

def add_japanese_articles():
    articles = []
    query = urllib.parse.quote("日本")
    all_articles_url = f"{base_url}search?q={query}&lang=ja&apikey={NEWS_API_ORG_API_KEY}"
    articles += add_all_articles(all_articles_url)
    for category in categories:
        time.sleep(1)
        category_url = f"{base_url}top-headlines?topic={category}&lang=ja&apikey={NEWS_API_ORG_API_KEY}"
        articles += add_headline_articles(category_url)
    return remove_duplicate_articles( articles )
                                                                            
if __name__ == '__main__':
    add_japanese_articles()