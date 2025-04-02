import tweepy

# Your Twitter API credentials
API_KEY = "qeZKAmaXsOefzgDF0PEdbxaJj"
API_SECRET = "wKpHbTEDMUiTDwp1lpX7efVDGEfueNZk3AABrwDMXqbXk3hCOE"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAMfOkAEAAAAAadjUpvtiNd3xES3xgukYR%2Bu3Pr0%3DECLXvPyPmDTKK1tcX7UwETQrHhGztyMKyuF496fRT9VjffpTMU"

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
