from gemini import runModel
from parseNews import fetch_news_content
from gNews import add_english_articles, add_japanese_articles
import datetime, time
from tweet import neutral_tweet, negative_tweet

promptsDict = {
    "extract" : "\nExtract only the article from the above text.",
    "isValidArticle" : "\nIs above text valid article?\nIf so reply True. If not reply False.",
    "isRelatedToJapan" : "\nIs the above text strongly related to Japan from Japan's view?\nIf so reply True. If not reply False.",
    "rewrite" : "\nRewrite the above text with Japan as topic.",
    "summarize" : "\nSummarize the above text in 70 words.",
    "translate" : "\n日本語に翻訳してください。",
    "finalizeContent" : "\nーツイート文章に直して\nー日本を中心にして\nー絵文字は使わないで\nー80文字ぐらいにして",
    "finalizeTitle" : "\n文章のタイトルを10文字ぐらいで書いて",
    "finalizeHeader" : "\5文字以内の状態を一つの単語で書いて",
    "isValidArticleJapanese" : "\n上の文章は記事として適切ですか?もしそうならTrue、そうでないならFalseを返してください。",
    "extractJapanese" : "\n上の文章から記事を抜き出して",
    "sadTweet" : "\n上の文章について日本への批判を100文字ぐらいで男性口調で書いて。"
}

articles = [{
    "title": "",
    "url": "",
    "date": ""
}]

today_utc = datetime.datetime.now(datetime.timezone.utc).date()

def create_neutral_tweet(article):
    article["final_content"] = runModel("pro", article["translated_summarized_content"] + promptsDict["finalizeContent"])
    article["final_title"] = runModel("pro", article["translated_summarized_content"] + promptsDict["finalizeTitle"])
    article["final_header"] = runModel("flash", article["translated_summarized_content"] + promptsDict["finalizeHeader"])
    article["final_header"] = article["final_header"].replace("\n", "")
    article["final_header"] = article["final_header"].replace(" ", "")
    article["final_header"] = '【' + article["final_header"] + '】'
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

            article["rewritten_text"] = runModel("flash", article["title"] + article["content"] + promptsDict["rewrite"])
            article["summarized_text"] = runModel("flash", article["rewritten_text"] + promptsDict["summarize"])
            article["translated_summarized_content"] = runModel("flash", article["summarized_text"] + promptsDict["translate"])

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
            article["final_content"] = runModel("flash", article["title"] + article["content"] + promptsDict["sadTweet"])
            negative_tweet(f"{article['final_content']}\n{article['url']}")
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    #neutral_main()
    negative_main()
