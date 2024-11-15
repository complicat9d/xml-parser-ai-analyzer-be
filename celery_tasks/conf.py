from celery import Celery
from celery.schedules import crontab

from config import settings

app = Celery("tasks", broker=settings.CELERY_BROKER_URL)

# Celery configuration
app.conf.update(
    CELERYBEAT_SCHEDULE={
        "fetch_xml_every_midnight": {
            "task": "app.tasks.fetch_and_process_xml",
            "schedule": crontab(hour="0", minute="0"),
        },
    },
    CELERY_RESULT_BACKEND="redis://localhost:6379/0",
)

app.conf.CELERYBEAT_SCHEDULE_FILE = "celerybeat-schedule"
app.conf.timezone = "UTC"
