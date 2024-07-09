import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz
from urllib.parse import urlparse, parse_qs

url = "https://twittrend.jp/"

trends = []

def fetch_trends():
    # Fetch the content of the URL with User-Agent header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code != 200:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
        return f"Failed to retrieve content. Status code: {response.status_code}"

    # Parse the content with Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    now_trends = soup.find('div', id='now')
    now_trends = now_trends.find_all('p', class_='trend')
    now_trends = [re.sub(r'[\d\s.]', '', trend.text) for trend in now_trends]
    return now_trends

if __name__ == "__main__":
    print(fetch_trends())