# News Aggregator and Twitter Bot

This project is a news aggregator and Twitter bot that fetches news articles, processes them using Google's Generative AI (Gemini), and posts tweets based on the processed content. It includes functionality for both neutral and negative sentiment tweets.

## Features

- Fetches news articles from various sources using the GNews API
- Processes articles using Google's Generative AI (Gemini)
- Translates non-Japanese articles to Japanese
- Posts tweets with neutral and negative sentiments
- Analyzes and criticizes trending topics on Twitter

## Components

1. `gemini.py`: Handles interaction with Google's Generative AI (Gemini) model
2. `gNews.py`: Fetches news articles using the GNews API
3. `main.py`: Main script that orchestrates the entire process
4. `parseNews.py`: Parses and extracts content from news articles
5. `tweet.py`: Handles posting tweets to Twitter

## Setup

1. Clone the repository
2. Install required dependencies:
   ```
   pip install google-generativeai tweepy python-dotenv beautifulsoup4 requests
   ```
3. Create a `.env` file in the project root with the following environment variables:
   ```
   GOOGLE_API_KEY=your_google_api_key
   NEWS_API_ORG_API_KEY=your_gnews_api_key
   NEUTRAL_CONSUMER_KEY=your_neutral_twitter_consumer_key
   NEUTRAL_CONSUMER_SECRET=your_neutral_twitter_consumer_secret
   NEUTRAL_ACCESS_TOKEN=your_neutral_twitter_access_token
   NEUTRAL_ACCESS_TOKEN_SECRET=your_neutral_twitter_access_token_secret
   NEGATIVE_CONSUMER_KEY=your_negative_twitter_consumer_key
   NEGATIVE_CONSUMER_SECRET=your_negative_twitter_consumer_secret
   NEGATIVE_ACCESS_TOKEN=your_negative_twitter_access_token
   NEGATIVE_ACCESS_TOKEN_SECRET=your_negative_twitter_access_token_secret
   ```

## Usage

Run the main script:

```
python main.py
```

This will:
1. Fetch trending topics and post critical tweets about them
2. Fetch and analyze popular tweets, posting critical responses
3. Fetch, process, and post neutral news articles
4. Fetch, process, and post negative sentiment news articles (commented out by default)

## Note

This project uses AI to generate content and post it on Twitter. Please use responsibly and in accordance with Twitter's terms of service and content policies.

## License

[MIT License](https://opensource.org/licenses/MIT)
