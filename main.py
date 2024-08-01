from gemini import runModel
from parseNews import fetch_news_content
import datetime
from tweet import tweet_text
from buzzTwitter import fetch_japanese_tweet, fetch_english_tweet
from gNews import add_english_articles
from parseNews import fetch_news_content

promptsDict = {
    "extract" : "\nExtract only the article from the above text.",
    "isValidArticle" : "\nIs above text, an article?\nIf so reply True. If not reply False.",
    "translate" : "\n日本語に翻訳してください。",
    "extractJapanese" : "\n上の文章から記事を抜き出して",
    "criticizeJapaneseTweet" : "\n上のツイートを100文字ぐらいで男性口調で徹底的に批判して",
    "finalizeTweet": "\nーツイート文章に直して\nー100文字ぐらいにして",
    "criticizeEnglishTweet": "\nCriticize the above tweet"
}

seduceList = [
    "いつも頑張ってる君へ、ご褒美あげないとね。…何がいい？可愛いお口で言ってご覧。何でもしてあげるよ。",
    "イイコイイコ。よしよし。毎日お疲れ様。たまにはたくさん甘えていいんだよ。",
    "ぎゅー。…どう？充電された？足りなかったら遠慮せず言ってね。いくらでもぎゅーってしてあげるから。",
    "可愛いなぁ…。ん？可愛いなぁって思って。顔もそうだけど、存在そのものが可愛いの。",
    "無理は禁物。あなたに何かあったら、私すっごく悲しいから。…絶対、無理しないでね。",
    "ずっと傍にいたい。傍にいて、あなたの力になりたい。役に立ちたい。あなたにとって、特別でありたいの。",
    "いっぱい好き。たくさん、たっくさん好き。すーっごく好き。…幾ら行っても足りないくらい、好き。",
    "泣いていいよ。辛いときは泣いていい。でもね、その涙を拭うのも、笑顔にさせるのも、私の役割にしてね。誰にも譲らないからね。",
    "すりすり…あー、かぁいいなぁ…すりすり。…もう、可愛くて可愛くて、食べちゃいたい。",
    "はい、あーん。…美味しい？じゃあこっちも、あーん。…ふふっ、だぁめ、やめない。こうして甘やかすの楽しいもん。ほら、次行くよ？あーん。",
    "よしよし。大丈夫。君がいつも頑張ってること、私は知ってるから。たまには肩の力抜いて、楽になりなよ？",
    "やだ。だーめ。まーだ。…ぎゅうしたりない。もっともーっと、いっぱいギューってしたい。甘やかしたい。私の特権だもん。",
    "だめよ、そんなにこんつめすぎちゃ。可愛いお顔にくまさんできちゃうよ？私の大事な人なんだから、もっと大事にしてよね。",
    "こっちおいで。マッサージしてあげる。…ふふっ。だいじょーぶ。変なことはしないから。…たぶん、ね。",
    "頑張り屋さんの君だから、これからもたっくさん色んなことを頑張るのよね。でも、私がいること忘れないでね。",
    "いつでも側にいるから、ちゃんと頼ってね。頼られないと、寂しいから。気軽に頼ってきてね。約束よ？",
    "おかえりなさい。今日も疲れたでしょ？ご飯できてるよ。それともお風呂がいい？それとも…私と、いっぱいイチャイチャする？",
    "ねぇ、ちゅーする？…ちゅー！うふふ！…ねぇえ？…もっと、する？",
    "キミがもやもやしてるの、いやだなぁ。…キミの笑顔が好きだから、好きなキミが笑顔でいてほしいから。力になりたい。",
    "おやすみなさい。今日も一日お疲れ様。いつもいつも頑張って偉いね。よしよし。…大好きだよ。いい夢見てね。",
    "立ち止まらずに頑張り続けられるなんて、本当にすごい。でもね、たまには立ち止まってもいいのよ？立ち止まって、休憩して。頑張り続けなくていいの。",
    "眠くなったら、このまま一緒に眠りましょ？それまで、ずっとこうしているわね。いい子、いい子。",
    "今日もたくさん頑張ったのかしら？頑張り屋さんのあなただもの。分かるわよ。頑張りすぎないで、って言っても頑張りすぎちゃう困ったさん？そんなところも素敵だけれど、あんまり無理はしないでね。",
    "よしよし……よく頑張りました。えらいえらい。いつも気を張って、ずっと走り続けているの、私は知ってるわよ。"
]

articles = [{
    "title": "",
    "url": "",
    "date": ""
}]

today_utc = datetime.datetime.now(datetime.timezone.utc).date()

def news_main():
    articles = add_english_articles()
    for article in articles:
        try:
            news_content = fetch_news_content(article["url"])
            article["content"] = runModel("flash", news_content + promptsDict["extract"])
            if "True" not in runModel("flash", article["content"] + promptsDict["isValidArticle"]):
                continue
            article["translated_content"] = runModel("flash", article["content"] + promptsDict["translate"])
            article["final_content"] = runModel("flash", article["translated_content"] + promptsDict["finalizeTweet"])
            if len(f"{article['final_content']}") <= 117:
                tweet_text("neutral", f"{article['final_content']}\n{article['url']}")
        except Exception as e:
            print(e)
            continue

def japaneseTwitter_negative():
    buzz_tweets = fetch_japanese_tweet()
    for tweet in buzz_tweets:
        print(tweet)
        try:
            content = runModel("flash", tweet["twitter_text"] + promptsDict["criticizeJapaneseTweet"])
            if len(content) <= 117:
                tweet_text("japanese_negative", f"{content}\n{tweet['tweet_url']}")
        except Exception as e:
            print(e)
            continue

def seduce_tweet():
    buzz_tweets = fetch_japanese_tweet()
    for tweet in buzz_tweets:
        promptsDict["seduce"] = ""
        for seduce in seduceList:
            promptsDict["seduce"] += f"彼女：{seduce}\n"
        promptsDict["seduce"] += f"ツイート文に対してセクシーに短く誘惑して\n"
        try:
            promptsDict["seduce"] += f"ツイート文：{tweet['twitter_text']}\n"
            content = runModel("flash", promptsDict["seduce"] + "彼女：")
            if len(content) <= 117:
                tweet_text("japanese_seduce", f"{content}\n{tweet['tweet_url']}")
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    japaneseTwitter_negative()
    news_main()
    seduce_tweet()