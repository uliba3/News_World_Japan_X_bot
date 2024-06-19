set -e
IMAGE_TAG=${1:-latest}
docker build -t uliba/news_twitter_bot:$IMAGE_TAG .
docker push uliba/news_twitter_bot:$IMAGE_TAG
