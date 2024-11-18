from celery import Celery
from celery.schedules import crontab

from celery_tasks.tasks import fetch_and_process_sales_data  # noqa
from config import settings

app = Celery("tasks")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND_URL

app.conf.beat_schedule_filename = "celerybeat-schedule"
app.conf.update(
    beat_schedule={
        "fetch_xml_every_midnight": {
            "task": "data:fetch",
            "schedule": crontab(hour="0", minute="0"),
        },
    },
    timezone="UTC",
    broker_connection_retry_on_startup=True,
)
