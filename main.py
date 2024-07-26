from gemini import runModel
from parseNews import fetch_news_content
import datetime
from tweet import tweet_text
from buzzTwitter import fetch_buzz_tweet, fetch_buzz_tweet_text
from footballNews import get_football_news

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
    "criticizeTweet" : "\n上のツイートを100文字ぐらいで男性口調で徹底的に批判して",
    "finalizeFootballTweet": "\nーツイート文章に直して\nー100文字ぐらいにして",
    "analyzeTweet": "\n上のツイートが話題になった理由を100文字でツイッター専門家として冷静に分析して",
    "adviseTweet": "\n上のツイートの改善できる部分を100文字で書いて",
}

articles = [{
    "title": "",
    "url": "",
    "date": ""
}]

today_utc = datetime.datetime.now(datetime.timezone.utc).date()

def football_main():
    football_news = get_football_news()
    for article in football_news:
        try:
            news_content = fetch_news_content(article["url"])
            article["content"] = runModel("flash", news_content + promptsDict["extract"])
            if "True" not in runModel("flash", article["content"] + promptsDict["isValidArticle"]):
                continue

            article["translated_content"] = runModel("flash", article["content"] + promptsDict["translate"])

            article["final_content"] = runModel("flash", article["translated_content"] + promptsDict["finalizeFootballTweet"])
            if len(f"{article['final_content']}") <= 117:
                tweet_text("neutral", f"{article['final_content']}\n{article['url']}")
        except Exception as e:
            print(e)
            continue

def buzzTwitter_negative():
    buzz_tweets = fetch_buzz_tweet()
    for tweet in buzz_tweets:
        print(tweet)
        try:
            content = runModel("flash", tweet["twitter_text"] + promptsDict["criticizeTweet"])
            if len(content) <= 117:
                tweet_text("negative", f"{content}\n{tweet['tweet_url']}")
        except Exception as e:
            print(e)
            continue

def buzzTwitter_analysis():
    buzz_tweets = fetch_buzz_tweet_text()
    for tweet in buzz_tweets:
        print(tweet)
        try:
            content = runModel("flash", tweet["twitter_text"] + promptsDict["analyzeTweet"])
            if len(content) <= 117:
                tweet_text("analysis", f"{content}\n{tweet['tweet_url']}")
            content = runModel("flash", tweet["twitter_text"] + promptsDict["adviseTweet"])
            if len(content) <= 117:
                tweet_text("analysis", f"{content}\n{tweet['tweet_url']}")
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    buzzTwitter_negative()
    football_main()
    buzzTwitter_analysis()