#!/bin/bash

# Delete the celerybeat-schedule file if it exists
if [ -f "celerybeat-schedule" ]; then
    rm celerybeat-schedule
    echo "Deleted existing celerybeat-schedule file"
fi

# Start Redis server and store its PID
redis-server &
REDIS_PID=$!

# Start Celery worker and store its PID
celery -A celery_app worker --loglevel=info &
CELERY_WORKER_PID=$!

# Start Celery Beat and store its PID
celery -A celery_app beat --loglevel=info &
CELERY_BEAT_PID=$!

# Function to stop services
stop_services() {
    echo "Stopping Celery Beat..."
    kill $CELERY_BEAT_PID
    echo "Stopping Celery Worker..."
    kill $CELERY_WORKER_PID
    echo "Stopping Redis Server..."
    kill $REDIS_PID
}

# Trap EXIT signal to stop services when the script exits
trap stop_services EXIT

# Wait for the background processes to finish
wait
