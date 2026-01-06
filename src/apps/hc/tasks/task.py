"""
Health Checker - Tasks - Keep alive.
"""

from src.libs.celery import celery
from src.libs.celery.utils import handle_error


@handle_error
@celery.task
def task() -> bool:
    """
    Keep the service alive.
    """

    print("Keeping the service alive...")

    return True
