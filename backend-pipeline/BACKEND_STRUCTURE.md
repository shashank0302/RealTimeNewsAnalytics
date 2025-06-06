# Backend Structure Overview

> 📌 **Note**: This directory structure has been implemented! Check `VISUAL_STRUCTURE.txt` for a visual tree view.

## 📁 Directory Organization

```
backend-pipeline/
├── djangoBackend/          # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   ├── celery.py          # Celery configuration
│   └── wsgi.py            # WSGI application
│
├── api/                    # Main application code
│   ├── models.py          # Database models
│   ├── views.py           # API endpoints
│   ├── serializers.py     # API serialization
│   ├── tasks.py           # Celery tasks & analytics
│   ├── urls.py            # API routes
│   └── analytics/         # Analytics modules (NEW)
│       ├── __init__.py
│       ├── sentiment.py   # Sentiment analysis
│       └── summarizer.py  # Text summarization
│
├── BackendTests/          # Test suite
├── manage.py              # Django management
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
└── run.sh               # Startup script
```

## 🔧 Component Separation

### 1. Core Backend (What Analytics Devs Touch)
- **Location**: `api/` directory
- **Purpose**: Business logic, data processing, analytics
- **Key Files**:
  - `models.py` - Data structures
  - `views.py` - API endpoints
  - `tasks.py` - Processing logic
  - `analytics/` - Analytics modules

### 2. Infrastructure (Rarely Modified)
- **Celery Config**: `djangoBackend/celery.py`
- **Redis**: Used for task queue & caching
- **PostgreSQL**: Main database
- **Docker**: Container configuration

### 3. Development Separation

When developing analytics:
- ✅ Work in `api/` directory
- ✅ Add new modules in `api/analytics/`
- ✅ Update `models.py` for new fields
- ✅ Update `tasks.py` for processing
- ❌ Don't modify infrastructure files

## 🚀 Quick Development Tips

1. **Analytics code goes in `api/analytics/`**
   ```python
   # api/analytics/your_feature.py
   def your_analytics_function(data):
       # Your code here
       return processed_data
   ```

2. **Import in tasks.py**
   ```python
   # api/tasks.py
   from .analytics.your_feature import your_analytics_function
   ```

3. **Test with Django shell**
   ```bash
   docker-compose exec backend python manage.py shell
   >>> from api.analytics.your_feature import your_analytics_function
   >>> result = your_analytics_function(test_data)
   ```

## 📝 Adding New Analytics Features

1. Create module in `api/analytics/`
2. Add model fields if needed
3. Update task processing
4. Add API endpoint if needed
5. Test with shell/API

The modular structure keeps analytics code separate from infrastructure! 