# Docker Setup for Globe News Application

This README provides instructions for running the application using Docker.

## Prerequisites

- Docker
- Docker Compose

## Setup and Running

### 1. Build and Start All Services

```bash
docker-compose up -d
```

This will build and start all services:
- Frontend React application (http://localhost:3000)
- Backend Django API (http://localhost:8000)
- Redis (internal port 6379)
- Celery Worker (for task processing)
- Celery Beat (for scheduled tasks)
- Flower dashboard (http://localhost:5555) for monitoring Celery tasks

### 2. View Logs

```bash
# View logs from all services
docker-compose logs -f

# View logs from a specific service
docker-compose logs -f backend
docker-compose logs -f celery_worker
```

### 3. Accessing the Services

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Flower Dashboard: http://localhost:5555

### 4. Running Commands Inside Containers

```bash
# Run Django management commands
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# Run npm commands
docker-compose exec frontend npm install some-package
```

### 5. Stopping the Services

```bash
docker-compose down
```

### 6. Rebuilding After Changes to Dockerfile

```bash
docker-compose build
docker-compose up -d
```

## Environment Variables

Environment variables are stored in the `.env` file. You can modify them as needed.

## Data Persistence

- Redis data is not persisted by default.
- If you need database persistence, add a database service like PostgreSQL to the docker-compose.yml file.

## Monitoring Celery Tasks

Celery tasks can be monitored through the Flower dashboard at http://localhost:5555. 