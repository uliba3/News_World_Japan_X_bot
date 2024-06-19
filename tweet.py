import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bearer token from environment variables
bearer_token = os.getenv("BEARER_TOKEN")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)

def write_news_tweet(title, url, content):
    tweet_text = f"{title}{url}\n\n{content}"
    print(tweet_text)
    response = client.create_tweet(
        text=tweet_text
    )

if __name__ == '__main__':
    write_news_tweet("【参加】日本、グローバルAI安全ネットワークへ ", "https://www.wired.com/story/us-forming-global-ai-safety-network-key-allies/", "日本、米国、英国、カナダ、シンガポール、欧州AIオフィスとともにグローバルAI安全ネットワークに参加。AIリスクの評価・軽減、責任あるAI開発を推進する国際的な取り組みです。 ")