# RealTimeNewsAnalytics

RealTimeNewsAnalytics is a full‑stack web application for collecting and analyzing news articles from various sources in real time. The project consists of a Django backend and a React frontend. Celery workers handle background tasks such as fetching articles and cleaning old data. The entire stack can be run locally using Docker Compose.

## Features

- **Django API** – exposes endpoints to retrieve processed news by country.
- **Celery tasks** – scheduled jobs fetch news feeds, process the data, and remove old records.
- **React frontend** – simple interface bootstrapped with Create React App.
- **Docker setup** – development environment including PostgreSQL, Redis, Celery worker/beat and a Flower dashboard.

## Getting Started

1. Ensure you have Docker and Docker Compose installed.
2. Build and start the services:

```bash
docker-compose up -d
```

This launches the backend at `http://localhost:8000` and the frontend at `http://localhost:3000`.

## Useful Commands

- View logs from all services:
  ```bash
  docker-compose logs -f
  ```
- Run Django management commands inside the backend container:
  ```bash
  docker-compose exec backend python manage.py migrate
  docker-compose exec backend python manage.py createsuperuser
  ```
- Stop all services:
  ```bash
  docker-compose down
  ```

For additional Docker notes see `DOCKER_README.md`.
