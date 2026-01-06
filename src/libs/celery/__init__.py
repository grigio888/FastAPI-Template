"""
Celery initialization module.
"""

from celery import Celery

from src.libs.celery import config
from src.settings import Settings

redis_url = f"redis://{Settings.REDIS_HOST}:{Settings.REDIS_PORT}/1"

celery = Celery(
    "worker",
    backend=redis_url,
    broker=redis_url,
)

celery.config_from_object(config, silent=False, force=True)
