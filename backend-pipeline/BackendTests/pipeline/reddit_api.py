import os
import praw

# Load Reddit API credentials from environment variables
CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "buzznet/1.0")

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

def fetch_reddit_posts(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.new(limit=limit)
    return [{"title": post.title, "content": post.selftext} for post in posts]

# Test the function
if __name__ == "__main__":
    results = fetch_reddit_posts("business")
    for post in results:
        print(f"Title: {post['title']}\n")
