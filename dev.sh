#!/bin/bash

# Development Helper Script
# Makes it easy to run common development commands

case "$1" in
  "analytics")
    echo "🚀 Starting analytics development environment..."
    docker-compose --profile analytics up -d
    echo "✅ Backend available at: http://localhost:8000"
    echo "📊 Database available at: localhost:5432"
    echo "💡 Run 'docker-compose logs -f backend' to see logs"
    ;;
    
  "backend")
    echo "🔧 Starting backend development environment..."
    docker-compose --profile backend up -d
    echo "✅ Services started!"
    ;;
    
  "full")
    echo "🌐 Starting full application..."
    docker-compose --profile full up -d
    echo "✅ All services started!"
    echo "Frontend: http://localhost:3000"
    echo "Backend: http://localhost:8000"
    echo "Flower: http://localhost:5555"
    ;;
    
  "stop")
    echo "🛑 Stopping all services..."
    docker-compose down
    ;;
    
  "logs")
    docker-compose logs -f backend
    ;;
    
  "shell")
    docker-compose exec backend python manage.py shell
    ;;
    
  "migrate")
    docker-compose exec backend python manage.py migrate
    ;;
    
  "test")
    docker-compose exec backend python manage.py test api
    ;;
    
  "restart")
    echo "🔄 Restarting backend..."
    docker-compose restart backend
    ;;
    
  "build")
    echo "🔨 Rebuilding backend..."
    docker-compose build backend
    ;;
    
  *)
    echo "📋 Development Helper Commands:"
    echo ""
    echo "  ./dev.sh analytics  - Start analytics dev environment (backend+db+redis)"
    echo "  ./dev.sh backend    - Start backend dev environment"
    echo "  ./dev.sh full       - Start full application"
    echo "  ./dev.sh stop       - Stop all services"
    echo "  ./dev.sh logs       - View backend logs"
    echo "  ./dev.sh shell      - Open Django shell"
    echo "  ./dev.sh migrate    - Run database migrations"
    echo "  ./dev.sh test       - Run tests"
    echo "  ./dev.sh restart    - Restart backend"
    echo "  ./dev.sh build      - Rebuild backend image"
    echo ""
    ;;
esac 