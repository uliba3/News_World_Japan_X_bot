FROM python:3.9

RUN apt-get update && apt-get install -y ntpdate

# Install tweepy
RUN pip install tweepy python-dotenv google-generativeai requests beautifulsoup4

# Add your remaining Dockerfile instructions here

