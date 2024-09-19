#!/bin/bash

# Delete the celerybeat-schedule file if it exists
if [ -f "celerybeat-schedule" ]; then
    rm celerybeat-schedule
    echo "Deleted existing celerybeat-schedule file"
fi

# Start Celery Beat
celery -A celery_app beat --loglevel=info