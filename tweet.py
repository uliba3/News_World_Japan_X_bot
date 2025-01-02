import tweepy
import os
from dotenv import load_dotenv
import datetime
import pytz

# Load environment variables from .env file
load_dotenv()

# Get the bearer token from environment variables
neutral_consumer_key = os.getenv("NEUTRAL_CONSUMER_KEY")
neutral_consumer_secret = os.getenv("NEUTRAL_CONSUMER_SECRET")
neutral_access_token = os.getenv("NEUTRAL_ACCESS_TOKEN")
neutral_access_token_secret = os.getenv("NEUTRAL_ACCESS_TOKEN_SECRET")

neutral_client = tweepy.Client(
    consumer_key=neutral_consumer_key, consumer_secret=neutral_consumer_secret,
    access_token=neutral_access_token, access_token_secret=neutral_access_token_secret
)

def neutral_tweet(text):
    tweet_text("neutral_client", text)

negative_consumer_key = os.getenv("NEGATIVE_CONSUMER_KEY")
negative_consumer_secret = os.getenv("NEGATIVE_CONSUMER_SECRET")
negative_access_token = os.getenv("NEGATIVE_ACCESS_TOKEN")
negative_access_token_secret = os.getenv("NEGATIVE_ACCESS_TOKEN_SECRET")

japanese_negative_client = tweepy.Client(
    consumer_key=negative_consumer_key, consumer_secret=negative_consumer_secret,
    access_token=negative_access_token, access_token_secret=negative_access_token_secret
)

def negative_tweet(text):
    tweet_text("negative_client", text)

analysis_consumer_key = os.getenv("ANALYSIS_CONSUMER_KEY")
analysis_consumer_secret = os.getenv("ANALYSIS_CONSUMER_SECRET")
analysis_access_token = os.getenv("ANALYSIS_ACCESS_TOKEN")
analysis_access_token_secret = os.getenv("ANALYSIS_ACCESS_TOKEN_SECRET")

japanese_seduce_client = tweepy.Client(
    consumer_key=analysis_consumer_key, consumer_secret=analysis_consumer_secret,
    access_token=analysis_access_token, access_token_secret=analysis_access_token_secret
)

def analysis_tweet(text):
    tweet_text("analysis", text)

client = {}

client["neutral"] = neutral_client
client["japanese_negative"] = japanese_negative_client
client["japanese_seduce"] = japanese_seduce_client

def tweet_text(client_name, text):
    print(f"text: {text}")
    response = client[client_name].create_tweet(
        text=text,
        user_auth=True
    )

if __name__ == "__main__":
    analysis_tweet("Hello, world!")