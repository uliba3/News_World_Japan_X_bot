import requests
from bs4 import BeautifulSoup
import re
import datetime
import pytz
from urllib.parse import urlparse, parse_qs

urls = ["https://buzzweet.com/text-tweet/", "https://buzzweet.com/photo-tweet/", "https://buzzweet.com/video-tweet/", "https://buzzweet.com/cosme-tweet/"]

english_urls = ["https://buzzweet.com/en-tweet/", "https://buzzweet.com/en-tweet/2/"]

twitter_containers = [{
    "twitter_id": "twitter_id",
    "twitter_date" : "twitter_date",
    "twitter_text": "twitter_text",
    "tweet_id" : "tweet_id",
    "tweet_url" : "tweet_url"
}]


today_utc = datetime.datetime.now(datetime.timezone.utc).date()
yesterday_utc = today_utc - datetime.timedelta(days=1)

def parse_twitter_id(twitter_id_text):
    return re.sub(r'[\n@]', '', twitter_id_text)

def parse_twitter_date(twitter_date_text):
    # Given date and time in JST
    jst_time_str = twitter_date_text
    current_year = datetime.datetime.now().year
    # Convert the given string to a format that can be parsed
    jst_time_str_formatted = f"{current_year}年" + jst_time_str.replace("月", "-").replace("日・", "-").replace("時", ":").replace("分", "")
    
    # Parse the date and time
    jst_datetime = datetime.datetime.strptime(jst_time_str_formatted, "%Y年%m-%d-%H:%M")

    # Set the timezone to JST
    jst_timezone = pytz.timezone("Asia/Tokyo")
    jst_datetime = jst_timezone.localize(jst_datetime)

    # Convert to UTC
    utc_datetime = jst_datetime.astimezone(pytz.utc)
    return utc_datetime.date()

def parse_twitter_text(twitter_text):
    return twitter_text.replace("\n", "")

def fetch_tweet(urls, utc_date):
    # Fetch the content of the URL
    twitter_containers = []

    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to retrieve content. Status code: {response.status_code}"

        # Parse the content with Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all elements with class "twitter_container"
        twitter_ids = soup.find_all(class_="twitter_id")
        twitter_dates = soup.find_all(class_="twitter_date")
        twitter_texts = soup.find_all(class_="twitter_text")
        a_tags = soup.find_all('div', class_='twitter_button')

        for length in range(len(twitter_ids)):
            twitter_id = parse_twitter_id(twitter_ids[length].text)
            twitter_date_span = twitter_dates[length].find('span')
            twitter_date = twitter_date_span.text if twitter_date_span else ""
            twitter_date = parse_twitter_date(twitter_date)
            if url in urls and twitter_date != utc_date:
                continue

            twitter_text = twitter_texts[length].text
            twitter_text = parse_twitter_text(twitter_text)

            a_tag = a_tags[length].find('a')
            tweeturl = a_tag['href']
            parsed_url = urlparse(tweeturl)
            query_params = parse_qs(parsed_url.query)
            tweet_id = query_params.get('in_reply_to', [None])[0]
            twitter_containers.append({
                "twitter_date" : twitter_date,
                "twitter_text": twitter_text,
                "tweet_url" : f"https://x.com/{twitter_id}/status/{tweet_id}",
                "tweet_type_url": url
            })
    return twitter_containers

def fetch_english_tweet():
    return fetch_tweet(english_urls, today_utc)

def fetch_japanese_tweet():
    return fetch_tweet(urls, yesterday_utc)

def fetch_japanese_text_tweet():
    return fetch_tweet([urls[0]], yesterday_utc)
