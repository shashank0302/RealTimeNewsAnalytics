import praw

# Your Reddit API credentials
CLIENT_ID = "QtpJhmymZH1H4k-c3nbFYQ"
CLIENT_SECRET = "IIJc1uQbf_mGyAL_fgzclcYPljFuAQ"
USER_AGENT = "buzznet/1.0"

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
