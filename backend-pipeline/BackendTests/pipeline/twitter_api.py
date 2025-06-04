import os
import tweepy

# Load Twitter API credentials from environment variables
API_KEY = os.environ.get("TWITTER_API_KEY")
API_SECRET = os.environ.get("TWITTER_API_SECRET")
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

# Authenticate
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_tweets(query, max_results=10):
    tweets = client.search_recent_tweets(query=query, max_results=max_results)
    return tweets.data

# Test the function
if __name__ == "__main__":
    results = fetch_tweets("#business")
    for tweet in results:
        print(tweet.text)
