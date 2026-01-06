"""
Health Checker - Tasks module.

This module defines the imports and beat schedule from health checker tasks to be
included on the Celery app.
"""

from celery.schedules import crontab

imports: list[str] = [
    "src.apps.hc.tasks.task",
]

beat_schedule: dict[str, dict] = {
    "run_health_check_keep_alive": {
        "task": "src.apps.hc.tasks.task",
        "schedule": crontab(minute="*"),  # every minute
        # "schedule": crontab(minute='*'),  # every minute  # noqa: ERA001
    },
}
