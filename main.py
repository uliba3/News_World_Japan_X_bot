from gemini import runModel
from parseNews import fetch_news_content
from gNews import add_articles
import datetime, time
from tweet import neutral_tweet

promptsDict = {
    "extract" : "\nExtract only the article from the above text.",
    "isValidArticle" : "\nIs above text valid article?\nIf so reply True. If not reply False.",
    "isRelatedToJapan" : "\nIs the above text strongly related to Japan from Japan's view?\nIf so reply True. If not reply False.",
    "rewrite" : "\nRewrite the above text with Japan as topic.",
    "summarize" : "\nSummarize the above text in 70 words.",
    "translate" : "\n日本語に翻訳してください。",
    "finalizeContent" : "\nーツイート文章に直して\nー日本を中心にして\nー絵文字は使わないで\nー80文字ぐらいにして",
    "finalizeTitle" : "\n文章のタイトルを15文字ぐらいで書いて",
    "finalizeHeader" : "\n5文字以内の状態を書いて"
}

articles = [{
    "title": "",
    "url": "",
    "date": ""
}]

def create_neutral_tweet(article):
    article["final_content"] = runModel("pro", article["translated_summarized_content"] + promptsDict["finalizeContent"])
    article["final_title"] = runModel("pro", article["translated_summarized_content"] + promptsDict["finalizeTitle"])
    article["final_header"] = runModel("flash", article["translated_summarized_content"] + promptsDict["finalizeHeader"])
    article["final_header"] = article["final_header"].replace("\n", "")
    article["final_header"] = '【' + article["final_header"] + '】'
    neutral_tweet(f"{article['final_header']}{article['final_title']}{article['url']}\n{article['final_content']}")

if __name__ == "__main__":
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    articles = add_articles()
    for article in articles:
        if article['date'] != today_utc:
            continue
        try:
            news_content = fetch_news_content(article["url"])
            print("1")
            article["content"] = runModel("flash", news_content + promptsDict["extract"])
            print("2")
            if "True" not in runModel("flash", article["content"] + promptsDict["isValidArticle"]):
                continue

            article["rewritten_text"] = runModel("flash", article["content"] + promptsDict["rewrite"])
            article["summarized_text"] = runModel("flash", article["rewritten_text"] + promptsDict["summarize"])
            article["translated_summarized_content"] = runModel("flash", article["summarized_text"] + promptsDict["translate"])

            create_neutral_tweet(article)
        except Exception as e:
            print(e)
            continue
