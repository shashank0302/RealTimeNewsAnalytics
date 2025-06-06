# Development Setup for New Contributors

## Quick Start for Teammates

### Prerequisites
- **Docker Desktop** ([Download here](https://www.docker.com/products/docker-desktop/)) - REQUIRED
- Git
- VS Code (recommended)

#### Docker Desktop Installation:
1. Download from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Install and restart your computer
3. Launch Docker Desktop
4. Verify installation: `docker --version` and `docker-compose --version`

### 1. Clone and Setup (5 minutes)
```bash
git clone <your-repo-url>
cd Project
cp .env.example .env  # Add your API keys here
```

### 2. One-Command Start
```bash
docker-compose up -d
```

### 3. Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **Flower (Celery Monitor)**: http://localhost:5555
- **PgAdmin (Database)**: http://localhost:2200

### 4. Development Workflow

#### For Analytics Features (Sentiment Analysis, Summarization)
1. **Backend Changes**: Edit files in `backend-pipeline/api/`
2. **Add Dependencies**: Update `backend-pipeline/requirements.txt`
3. **Restart Backend**: `docker-compose restart backend celery_worker`
4. **View Logs**: `docker-compose logs -f backend`

#### For Frontend Changes
1. **Edit Files**: Changes in `frontend/src/` auto-reload
2. **Add Packages**: `docker-compose exec frontend npm install <package>`

### 5. Useful Commands
```bash
# View all logs
docker-compose logs -f

# Run Django commands
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py shell

# Restart specific service
docker-compose restart backend

# Rebuild after Dockerfile changes
docker-compose build backend
```

### 6. Analytics Development Areas

#### Sentiment Analysis
- **Location**: `backend-pipeline/api/tasks.py`
- **Add to**: News processing pipeline
- **Libraries**: TextBlob, VADER, or Transformers

#### Summarization  
- **Location**: `backend-pipeline/api/models.py` (add summary field)
- **Processing**: `backend-pipeline/api/tasks.py`
- **Libraries**: Sumy, Transformers, or OpenAI API

#### New API Endpoints
- **File**: `backend-pipeline/api/views.py`
- **URLs**: `backend-pipeline/api/urls.py`

### 7. Git Workflow
```bash
git checkout -b feature/sentiment-analysis
# Make changes
git add .
git commit -m "Add sentiment analysis to news processing"
git push origin feature/sentiment-analysis
# Create Pull Request
```

## Docker Learning Resources (15 minutes)
- [Docker basics](https://docs.docker.com/get-started/)
- [Docker Compose tutorial](https://docs.docker.com/compose/gettingstarted/) 