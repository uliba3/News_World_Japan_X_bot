import requests
from bs4 import BeautifulSoup
import re

def fetch_news_content(url):
    # Fetch the content of the URL
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to retrieve content. Status code: {response.status_code}"

    # Parse the content with Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    main_content = soup
    if not main_content:
        return "Main content not found"

    # Extract and concatenate all paragraph texts within the main content section
    paragraphs = main_content.find_all('p')
    content = "\n".join([re.sub('<[^<]+?>', '', p.get_text()) for p in paragraphs])

    return content
