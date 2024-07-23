import json, os
import urllib.request

base_url = "https://footballnewsapi.netlify.app/.netlify/functions/api/news"

football_urls = ["/onefootball", "/espn", "/90mins", "/goal"]

def get_football_news():
    football_news = []
    for url in football_urls:
        with urllib.request.urlopen(base_url + url) as response:
            data = json.loads(response.read().decode("utf-8"))
            for i, article in enumerate(data):
                if i >= 5:
                    break
                print(article)
                if url != "/goal":
                    football_news.append({
                        "title": article['title'],
                        "url": article['url']
                    })
                else:
                    football_news.append({
                        "title": article['modifiedTitle3'],
                        "url": article['url']
                    })
    return football_news

if __name__ == '__main__':
    print(get_football_news())