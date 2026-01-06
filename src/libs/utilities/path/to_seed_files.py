"""
Utilities - Path - Seeds.

This module provides utility functions for working with file paths
and loading seed data for the database.
"""

from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.libs.utilities.path import load_all_objects_from

log = get_logger()


def load_all_seeds() -> list:
    """
    Load all seed functions from the seeds directory.

    Returns:
        list: A list of seed functions.

    """

    modules = load_all_objects_from("seeds", "seed_", only_modules=True)

    order_to_seed: list = []
    repeated_iteration = 0

    while modules:
        module = modules.pop(0)

        depends_on = getattr(module, "depends_on", [])
        current_seeds = {
            str(func.__name__).replace("seed_", "") for func in order_to_seed
        }

        if not depends_on or set(depends_on).issubset(current_seeds):
            if hasattr(module, "__all__"):
                order_to_seed.extend(getattr(module, item) for item in module.__all__)

            repeated_iteration = 0

        else:
            repeated_iteration += 1
            modules.append(module)

        if repeated_iteration == 10:
            log.warning(
                f"{_()}: Repeated iteration limit reached. "
                "A circular dependency may exist.",
            )
            break

    return order_to_seed
