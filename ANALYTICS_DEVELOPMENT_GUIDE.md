# Analytics Development Guide

## 🚀 Quick Start for Analytics Development

This guide helps you develop analytics features (sentiment analysis, summarization, etc.) without dealing with the full infrastructure stack.

## 📋 Development Profiles

We use Docker profiles to run only what you need:

| Profile | Services | Use Case |
|---------|----------|----------|
| `analytics` | Backend + DB + Redis | Core analytics development |
| `backend` | Backend + DB + Redis | General backend development |
| `celery` | Celery Worker + Beat + Flower | Background task development |
| `full` | All services | Full application testing |
| `infrastructure` | DB + Redis + Celery | Infrastructure only |

## 🔧 Common Development Workflows

### 1. Analytics Development (Most Common)
**For developing sentiment analysis, summarization, or other analytics features:**

```bash
# Start only backend services (Django + DB + Redis)
docker-compose --profile analytics up -d

# View backend logs
docker-compose logs -f backend

# Access services:
# - Backend API: http://localhost:8000
# - Database: localhost:5432
```

### 2. Quick Backend Restart (Hot Reload)
**When you modify Python code, Django auto-reloads:**

```bash
# Code changes are automatically detected!
# If you need to force restart:
docker-compose restart backend

# Or view live logs while coding:
docker-compose logs -f backend
```

### 3. Database Operations

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Django shell
docker-compose exec backend python manage.py shell

# Database shell
docker-compose exec db psql -U postgres
```

### 4. Testing Your Analytics Code

```bash
# Run specific analytics task manually
docker-compose exec backend python manage.py shell
>>> from api.tasks import your_analytics_function
>>> your_analytics_function()

# Run tests
docker-compose exec backend python manage.py test api.tests
```

## 📁 Where to Add Your Code

### Analytics Features Structure:

```
backend-pipeline/
├── api/
│   ├── models.py          # Add new fields (sentiment_score, summary)
│   ├── serializers.py     # Add new API fields
│   ├── views.py           # Add new API endpoints
│   ├── tasks.py           # Add analytics functions here
│   └── analytics/         # Create this for analytics modules
│       ├── __init__.py
│       ├── sentiment.py   # Sentiment analysis logic
│       └── summarizer.py  # Text summarization logic
```

### Example: Adding Sentiment Analysis

1. **Create analytics module:**
```python
# backend-pipeline/api/analytics/sentiment.py
from textblob import TextBlob

def analyze_sentiment(text):
    """Analyze sentiment of text."""
    blob = TextBlob(text)
    return {
        'polarity': blob.sentiment.polarity,
        'subjectivity': blob.sentiment.subjectivity,
        'sentiment': 'positive' if blob.sentiment.polarity > 0 else 'negative'
    }
```

2. **Update model:**
```python
# backend-pipeline/api/models.py
class NewsData(models.Model):
    # ... existing fields ...
    sentiment_score = models.FloatField(null=True, blank=True)
    sentiment_label = models.CharField(max_length=20, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
```

3. **Update task to process sentiment:**
```python
# backend-pipeline/api/tasks.py
from .analytics.sentiment import analyze_sentiment

def process_article(article_data):
    # ... existing code ...
    sentiment_result = analyze_sentiment(article_data['content'])
    article_data['sentiment_score'] = sentiment_result['polarity']
    article_data['sentiment_label'] = sentiment_result['sentiment']
    # ... save to database ...
```

## 🛠️ Useful Commands Reference

### Service Management
```bash
# Start analytics environment
docker-compose --profile analytics up -d

# Stop all services
docker-compose down

# Restart just backend
docker-compose restart backend

# View all running containers
docker-compose ps
```

### Debugging
```bash
# Interactive backend shell
docker-compose exec backend bash

# View Django logs
docker-compose logs -f backend

# Check for errors
docker-compose exec backend python manage.py check
```

### Package Management
```bash
# Add new Python package
echo "package-name==version" >> backend-pipeline/requirements.txt
docker-compose build backend
docker-compose restart backend
```

## 💡 Pro Tips

1. **Fast Development Loop:**
   - Use `--profile analytics` to skip frontend and Celery services
   - Django's auto-reload means no manual restarts needed
   - Keep `docker-compose logs -f backend` open in a terminal

2. **Testing Analytics:**
   - Use Django shell for quick testing
   - Create management commands for complex tasks
   - Use Jupyter notebooks for data exploration (connect to DB)

3. **Performance:**
   - Profile-based startup is 3x faster than full stack
   - Hot reload prevents rebuild delays
   - Use Redis for caching analytics results

## 🚨 Troubleshooting

### Backend won't start?
```bash
# Check logs
docker-compose logs backend

# Rebuild if needed
docker-compose build backend
```

### Database connection issues?
```bash
# Ensure DB is running
docker-compose --profile analytics ps

# Check DB logs
docker-compose logs db
```

### Need full stack for testing?
```bash
# Start everything
docker-compose --profile full up -d
```

## 📝 Example: Complete Analytics Feature

Here's how to add a complete summarization feature:

```python
# 1. Install dependencies
# Add to requirements.txt:
# sumy==0.11.0

# 2. Create summarizer
# api/analytics/summarizer.py
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer

def summarize_text(text, sentences_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return ' '.join([str(sentence) for sentence in summary])

# 3. Update model and task
# Then rebuild: docker-compose build backend
```

## 🎯 Next Steps

1. Start with `docker-compose --profile analytics up -d`
2. Open your code editor to `backend-pipeline/api/`
3. Start coding your analytics features!
4. View logs with `docker-compose logs -f backend`

Happy coding! 🚀 