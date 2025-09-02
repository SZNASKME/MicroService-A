#!/bin/bash
# Production startup script for Data Analytics Microservice

set -e

echo "🚀 Starting Data Analytics Microservice..."

# Load environment variables
if [ -f ".env.production" ]; then
    echo "📦 Loading production environment..."
    export $(grep -v '^#' .env.production | xargs)
fi

# Create required directories
echo "📁 Creating required directories..."
mkdir -p logs uploads

# Set proper permissions
chmod 755 logs uploads

# Install/update dependencies
echo "📋 Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Run database migrations (if needed in future)
# python migrate.py

# Start the application with Gunicorn
echo "🌟 Starting application with Gunicorn..."
exec gunicorn \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers ${WORKERS:-4} \
    --worker-class sync \
    --worker-connections ${WORKER_CONNECTIONS:-1000} \
    --max-requests ${MAX_REQUESTS:-1000} \
    --max-requests-jitter ${MAX_REQUESTS_JITTER:-100} \
    --timeout ${TIMEOUT:-30} \
    --keep-alive ${KEEP_ALIVE:-2} \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level ${LOG_LEVEL:-warning} \
    --capture-output \
    --enable-stdio-inheritance \
    wsgi:application
