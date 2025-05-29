from gemini import runModel
from parseNews import fetch_news_content
import datetime
from tweet import tweet_text
from gNews import add_english_articles, add_japanese_articles
from parseNews import fetch_news_content
import time  # Add time module import

promptsDict = {
    "extract" : {
        "en": "\nExtract only the article from the above text.",
        "ja": "\n上の文章から記事を抜き出して"
    },
    "isValidArticle" : {
        "en": "\nIs above text, an article?\nIf so reply True. If not reply False.",
        "ja": "\n上の文章は記事ですか？\n記事ならTrueを返してください。違う場合はFalseを返してください。"
    },
    "translate" : "\n日本語に翻訳してください。",
    "finalizeTweet": "\n一つの短いニュースタイトルにして"
}

articles = [{
    "title": "",
    "url": "",
    "date": ""
}]

today_utc = datetime.datetime.now(datetime.timezone.utc).date()

def news_main(start):
    articles = add_english_articles()
    print(f"Added {len(articles)} articles")
    count = 0
    for article in articles:
        start_time = time.time()  # Start timing
        print(f"took {start_time - start}")
        count += 1
        try:
            if article["date"] != today_utc:
                continue
            news_content = fetch_news_content(article["url"])
            if news_content.startswith("Failed to retrieve content"):
                print(f"Failed to fetch content for {article['url']}")
                continue
            article["content"] = runModel("flash", news_content + promptsDict["extract"][article["language"]])
            if "True" not in runModel("flash", article["content"] + promptsDict["isValidArticle"][article["language"]]):
                continue
            if article["language"] == "en":
                article["translated_content"] = runModel("flash", article["content"] + promptsDict["translate"])
            else:
                continue
            article["final_content"] = runModel("flash", article["translated_content"] + promptsDict["finalizeTweet"])
            article["final_content"] = article["final_content"].replace("*", "")
            article["final_content"] = article["final_content"].replace("#", "")
            if len(f"{article['final_content']}") <= 117:
                tweet_text("neutral", f"{article['final_content']}\n{article['url']}")
        except Exception as e:
            print(f"iterated {count} articles - took {time.time() - start_time:.2f} seconds {time.time() - start} seconds from beginning")
            print(e)
            continue
        print(f"iterated {count} articles - took {time.time() - start_time:.2f} seconds {time.time() - start} seconds from beginning")

if __name__ == "__main__":
    s = time.time()
    news_main(s)