# https://docs.python.org/3/library/json.html
# This library will be used to parse the JSON data returned by the API.
import json
import os
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request
# This library will be used to fetch the API.
import urllib.request
import datetime
from dotenv import load_dotenv

load_dotenv()
NEWS_API_ORG_API_KEY = os.getenv("NEWS_API_ORG_API_KEY")

all_articles_url = f"https://gnews.io/api/v4/search?q=japan&lang=en&apikey={NEWS_API_ORG_API_KEY}"
headline_articles_url = f"https://gnews.io/api/v4/top-headlines?q=japan&lang=en&apikey={NEWS_API_ORG_API_KEY}"

def add_all_articles():
    articles = []
    with urllib.request.urlopen(all_articles_url) as response:
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

def add_headline_articles():
    articles = []
    with urllib.request.urlopen(headline_articles_url) as response:
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

def add_articles():
    return remove_duplicate_articles(add_all_articles() + add_headline_articles())

if __name__ == '__main__':
    articles = add_articles()