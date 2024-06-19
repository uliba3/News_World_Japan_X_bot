# Import the Python SDK
import google.generativeai as genai
# Used to securely store your API key
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

modelFlash = genai.GenerativeModel('gemini-1.5-flash')
modelPro = genai.GenerativeModel('gemini-1.5-pro')

def rewriteInJapanView(article):
    prompt = """
Rewrite the above text with Japan as topic."""
    response = modelFlash.generate_content(article+prompt)
    print(article+prompt)
    return response.text

def summarizeArticle(article):
    prompt = """
summarize the above text in 70 words."""
    response = modelFlash.generate_content(article+prompt)
    print(article+prompt)
    return response.text

def extractArticle(article):
    prompt = """
extract only the article from the above text."""
    response = modelFlash.generate_content(article+prompt)
    print(article+prompt)
    return response.text

def isArticleValid(article):
    prompt = """
Is above text valid article?
If so reply True. If not reply False."""
    response = modelFlash.generate_content(article+prompt)
    print(article+prompt)
    return response.text

def isRelatedToJapan(article):
    prompt = """
Is the above text strongly related to Japan from Japan's view?
If so reply True. If not reply False."""
    response = modelFlash.generate_content(article+prompt)
    print(article+prompt)
    return response.text

def translate(article):
    prompt = """
日本語に翻訳してください。"""
    response = modelFlash.generate_content(article+prompt)
    print(article+prompt)
    return response.text

def finalizeArticle(article):
    prompt = """
ーツイート文章に直して
ー日本を中心にして
ー絵文字は使わないで
ー80文字ぐらいにして"""
    response = modelPro.generate_content(article+prompt)
    print(article+prompt)
    print(response.text)
    return response.text

def rewriteAritcle(article):
    article = rewriteInJapanView(article)
    article = summarizeArticle(article)
    article = translate(article)
    return article

def finalizeTitle(article):
    prompt = """ー下の文章のタイトルを書いて
ー初めに【<5文字以内で状態を表す>】と書いて
ー【速報】は書かないで
ー20文字ぐらいにして
"""
    response = modelPro.generate_content(prompt+article)
    print(prompt+article)
    print(response.text)
    return response.text