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

def add_all_articles(articles):
    with urllib.request.urlopen(all_articles_url) as response:
        data = json.loads(response.read().decode("utf-8"))
        all_articles = data["articles"]
    for article in all_articles:
        date = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()
        articles.append({
            "title": article['title'],
            "final_title": "",
            "url": article['url'],
            "date": date,
            "content": "",
            "translated_summarized_content" : "",
            "final_content": ""
        })
    return articles

def add_headline_articles(articles):
    with urllib.request.urlopen(headline_articles_url) as response:
        data = json.loads(response.read().decode("utf-8"))
        all_articles = data["articles"]
    for article in all_articles:
        date = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()
        articles.append({
            "title": article['title'],
            "final_title": "",
            "url": article['url'],
            "date": date,
            "content": "",
            "translated_summarized_content" : "",
            "final_content": ""
        })
    return articles

def remove_duplicate_articles(articles):
    seen_titles = set()
    for article in articles:
        if article['title'] in seen_titles:
            articles.remove(article)
        else:
            seen_titles.add(article['title'])
    return articles

def add_articles(articles):
    articles = add_all_articles(articles)
    articles = add_headline_articles(articles)
    articles = remove_duplicate_articles(articles)
    return articles

if __name__ == '__main__':
    articles = []
    articles = add_articles(articles)
    print(articles)