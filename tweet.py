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
    tweet(neutral_client, text)

negative_consumer_key = os.getenv("NEGATIVE_CONSUMER_KEY")
negative_consumer_secret = os.getenv("NEGATIVE_CONSUMER_SECRET")
negative_access_token = os.getenv("NEGATIVE_ACCESS_TOKEN")
negative_access_token_secret = os.getenv("NEGATIVE_ACCESS_TOKEN_SECRET")

negative_client = tweepy.Client(
    consumer_key=negative_consumer_key, consumer_secret=negative_consumer_secret,
    access_token=negative_access_token, access_token_secret=negative_access_token_secret
)

def negative_tweet(text):
    tweet(negative_client, text)

def tweet(client, text):
    print(f"text: {text}")
    response = client.create_tweet(
        text=text,
        user_auth=True
    )