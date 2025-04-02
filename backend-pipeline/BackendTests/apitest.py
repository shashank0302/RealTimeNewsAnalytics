import requests

# API_KEY = 'tQEhUNGhJmIMvqwqPxz5CmT2QYXNu6svPr7fO0fj'
# url = 'https://api.thenewsapi.com/v1/news/top'
# params = {
#     'api_token': API_KEY,
#     'locale': 'us',
#     'language': 'en',
#     'categories': 'business'
# }
# response = requests.get(url, params=params)
# data = response.json()
# print(data['data'])  # List of news articles
API_KEY = 'a7b501c964b0ac3f412cedabf6d035cc'
url = f'https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=us&max=10&apikey={API_KEY}'
response = requests.get(url)
data = response.json()
print(data['articles'])  # List of trending articles
