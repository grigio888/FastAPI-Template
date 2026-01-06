"""
Celery - Utils.
"""

from collections.abc import Callable
from functools import wraps

from src.libs.log import get_context as _
from src.libs.log import get_logger

log = get_logger()


def handle_error(
    func: Callable,
) -> Callable | None:
    """
    Log errors for the given function.

    Commonly used as a decorator for Celery tasks.
    """

    @wraps(func)
    def wrapped(*args: list, **kwargs: dict) -> Callable | None:
        try:
            return func(*args, **kwargs)
        except Exception:
            log.exception(f"{_()}: Error occurred in {func.__name__}")
            return None

    return wrapped
