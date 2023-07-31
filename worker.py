from celery import Celery
from utils.env import Env

env = Env()

app = Celery(
    "tasks",
    broker=env.get_value("CELERY_BROKER_URL"),
    backend=env.get_value("CELERY_RESULT_BACKEND"),
    include=["app.tasks.download_file", "app.tasks.delete_file"],
    broker_connection_retry_on_startup=True,
)
