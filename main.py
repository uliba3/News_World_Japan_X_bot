from gemini import runModel
from parseNews import fetch_news_content
from gNews import add_english_articles, add_japanese_articles
import datetime, time
from tweet import neutral_tweet, negative_tweet
from buzzTwitter import fetch_buzz_tweet

promptsDict = {
    "extract" : "\nExtract only the article from the above text.",
    "isValidArticle" : "\nIs above text, an article?\nIf so reply True. If not reply False.",
    "isRelatedToJapan" : "\nIs the above text related to Japan from Japan's view?\nIf so reply True. If not reply False.",
    "translate" : "\n日本語に翻訳してください。",
    "finalizeContent" : "\nーツイート文章に直して\nー日本を中心にして\nー絵文字は使わないで\nー80文字ぐらいにして",
    "finalizeTitle" : "\n文章のタイトルを10文字ぐらいで書いて",
    "finalizeHeader" : "\n上の記事を五文字以内の一つの単語で表して",
    "isValidArticleJapanese" : "\n上の文章は記事ですか?もしそうならTrue、そうでないならFalseを返してください。",
    "extractJapanese" : "\n上の文章から記事を抜き出して",
    "critisize" : "\n上のツイートを100文字ぐらいで男性口調で徹底的に批判して",
    "shorterJapanse" : "\n上の文章をトーンは同じで少し短くして",
}

articles = [{
    "title": "",
    "url": "",
    "date": ""
}]

today_utc = datetime.datetime.now(datetime.timezone.utc).date()
yesterday_utc = today_utc - datetime.timedelta(days=1)

def create_neutral_tweet(article):
    article["final_content"] = runModel("pro", article["translated_content"] + promptsDict["finalizeContent"])
    article["final_title"] = runModel("pro", article["final_content"] + promptsDict["finalizeTitle"])
    article["final_header"] = runModel("flash", article["final_content"] + promptsDict["finalizeHeader"])
    article["final_header"] = article["final_header"].replace("\n", "")
    article["final_header"] = article["final_header"].replace(" ", "")
    article["final_header"] = '【' + article["final_header"] + '】'
    strLength = len(f"{article['final_header']}{article['final_title']}\n\n{article['final_content']}")
    while strLength > 117:
        article["final_content"] = runModel("pro", article["final_content"] + promptsDict["shorterJapanse"])
        if strLength == len(f"{article['final_header']}{article['final_title']}\n\n{article['final_content']}"):
            break
    neutral_tweet(f"{article['final_header']}{article['final_title']}{article['url']}\n\n{article['final_content']}")

def neutral_main():
    articles = add_english_articles()
    for article in articles:
        if article['date'] != today_utc:
            continue
        try:
            news_content = fetch_news_content(article["url"])
            article["content"] = runModel("flash", news_content + promptsDict["extract"])
            if "True" not in runModel("flash", article["content"] + promptsDict["isValidArticle"]):
                continue

            article["translated_content"] = runModel("flash", article["content"] + promptsDict["translate"])

            create_neutral_tweet(article)
        except Exception as e:
            print(e)
            continue

def negative_main():
    articles = add_japanese_articles()
    for article in articles:
        if article['date'] != today_utc:
            continue
        try:
            news_content = fetch_news_content(article["url"])
            article["content"] = runModel("flash", news_content + promptsDict["extractJapanese"])
            if "True" not in runModel("flash", article["content"] + promptsDict["isValidArticleJapanese"]):
                continue
            if "True" not in runModel("flash", article["content"] + promptsDict["isRelatedToJapan"]):
                continue
            article["final_content"] = runModel("pro", article["title"] + article["content"] + promptsDict["critisize"])
            strLength = len(article["final_content"])
            while len(article["final_content"]) > 117:
                article["final_content"] = runModel("pro", article["final_content"] + promptsDict["shorterJapanse"])
                if strLength == len(article["final_content"]):
                    break
                strLength = len(article["final_content"])
            negative_tweet(f"{article['final_content']}\n{article['url']}")
        except Exception as e:
            print(e)
            continue

def buzzTwitter_main():
    buzz_tweets = fetch_buzz_tweet()
    for tweet in buzz_tweets:
        print(tweet)
        if tweet['twitter_date'] != yesterday_utc:
            print(today_utc)
            continue
        try:
            content = runModel("pro", tweet["twitter_text"] + promptsDict["critisize"])
            strLength = len(content)
            while len(content) > 117:
                content = runModel("pro", content + promptsDict["shorterJapanse"])
                if strLength == len(content):
                    break
                strLength = len(content)
            negative_tweet(f"{content}\n{tweet['tweet_url']}")
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    buzzTwitter_main()
    neutral_main()
    negative_main()
