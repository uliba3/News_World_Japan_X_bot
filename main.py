from gemini import isArticleValid, extractArticle, isRelatedToJapan, rewriteAritcle, finalizeArticle, finalizeTitle
from parseNews import fetch_news_content
from gNews import add_articles
import datetime, time
from tweet import write_news_tweet

articles = [{
    "title": "",
    "final_title": "",
    "url": "",
    "date": "",
    "content": "",
    "translated_summarized_content" : "",
    "final_content": ""
}]

if __name__ == "__main__":
    today = datetime.datetime.now().date()
    articles = []
    articles = add_articles(articles)
    for article in articles:
        if article['date'] != today:
            continue
        try:
            news_content = fetch_news_content(article["url"])
            article["content"] = extractArticle(article["title"]+news_content)
            if "True" not in isArticleValid(article["content"]):
                continue
            if "True" not in isRelatedToJapan(article["content"]):
                continue
            article["translated_summarized_content"] = rewriteAritcle(article["content"])
            article["final_content"] = finalizeArticle(article["translated_summarized_content"])
            article["final_title"] = finalizeTitle(article["translated_summarized_content"])
            write_news_tweet(article["final_title"], article["url"], article["final_content"])
            time.sleep(60)
        except Exception as e:
            print(e)
            time.sleep(60)
            continue
