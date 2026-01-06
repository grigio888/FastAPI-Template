"""
{{ cookiecutter.app_name.title() }} - Admin - Seeds.

This module contains the seed data for the {{ cookiecutter.app_name.title() }}.
"""

def seed_{{ cookiecutter.app_slug }}(param: int = 50) -> None:
    """
    Seed the {{ cookiecutter.app_name.title() }} table with initial data.

    """

    pass


# Depends On
# this defines the order of seeding. If any other seed should be done prior to this one,
# add them to the list below.
depends_on: list[str] = []

# All Exports
# this defines all exports for the module. this defines what will be auto imported
# by the app seeding utility.
__all__: list[str] = []