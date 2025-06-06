# 🚀 Analytics Developer Quick Start

## Start Development (Takes 30 seconds)
```bash
# Clone repo
git clone <repo-url>
cd Project

# Start analytics environment (Backend + DB only)
docker-compose --profile analytics up -d
```

## Your Workspace
```
backend-pipeline/api/
├── models.py          # Add new fields here
├── tasks.py           # Add processing logic here
└── analytics/         # Create your modules here
    ├── sentiment.py   # Your sentiment analysis
    └── summarizer.py  # Your summarization
```

## Common Commands
```bash
# View logs while coding
docker-compose logs -f backend

# Django shell for testing
docker-compose exec backend python manage.py shell

# Restart after installing packages
docker-compose restart backend

# Stop everything
docker-compose down
```

## Adding Analytics Example
```python
# 1. Create: backend-pipeline/api/analytics/sentiment.py
from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# 2. Use in: backend-pipeline/api/tasks.py
from .analytics.sentiment import analyze_sentiment

# In your processing function:
sentiment = analyze_sentiment(article_text)
```

## Hot Reload = No Restarts! 
- ✅ Edit Python files → Changes apply automatically
- ✅ View logs to see your print() statements
- ❌ Only rebuild for new packages

## Need Help?
- Full guide: `ANALYTICS_DEVELOPMENT_GUIDE.md`
- Backend structure: `backend-pipeline/BACKEND_STRUCTURE.md`

**Backend API:** http://localhost:8000/api/ 