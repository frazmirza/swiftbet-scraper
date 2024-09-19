from celery import Celery
from celery.schedules import crontab

# Initialize the Celery app
app = Celery('tasks', broker='redis://localhost:6379/0')

# Add your configurations (e.g., result backend if needed)
app.conf.result_backend = 'redis://localhost:6379/0'



app.conf.beat_schedule = {
    'run-race-scraper-every-2-minutes': {
        'task': 'tasks.run_race_scraper',
        'schedule': crontab(minute='*/2'),  # This will run every 2 minutes
    },
}

import tasks  # Ensure this import
