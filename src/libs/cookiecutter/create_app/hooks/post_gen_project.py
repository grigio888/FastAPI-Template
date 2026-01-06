import os
import sys
import textwrap

steps = [
    """Check your models file:
    - src/apps/{{ cookiecutter.app_slug }}/models.py
    - Ensure your model(s) are defined correctly.
""",
"""Migrate your database:
    - Run `make db-create-migration message="Add {{ cookiecutter.app_name }} models"` to
        create a new migration.
    - Note that the migration file will be created under `src/libs/database/migrations/`.
    - Run `make db-migrate` to apply the migration.
    - If anything goes wrong, you can always rollback with `make db-undo-migrate`.
""",
"""Check your schemas file:
    - src/apps/{{ cookiecutter.app_slug }}/schemas.py
    - Ensure your schema(s) are defined correctly.
    - The custom BaseModel provided has a `from_model` method to help you convert models
        to schemas.
""",
"""Check your endpoints file:
    - src/apps/{{ cookiecutter.app_slug }}/endpoints.py
    - Ensure your endpoint(s) are defined correctly and using the correct services.
""",
"""Check your services file:
    - src/apps/{{ cookiecutter.app_slug }}/services.py
    - Implement the business logic for your app here.
""",
"""Check your Admin file:
    - src/apps/{{ cookiecutter.app_slug }}/admin/__init__.py
    - Ensure your admin view(s) are defined correctly and using the correct model(s).
""",
"""Check your messages file:
    - src/apps/{{ cookiecutter.app_slug }}/messages.py
    - This module is already populated with a sample message class.
    - It relies on a localization system to provide messages in different languages.
""",
]

print("""----------------------------------------------------------------------
----------------------------------------------------------------------
----------------------------------------------------------------------
App created successfully!

This FastAPI application already auto discovers any app you create, so there's no need
to register it manually.
All endpoints, admins, models and tasks are auto discovered.

App Name: {{ cookiecutter.app_name }}
App Slug: {{ cookiecutter.app_slug }}

Files created:
    - src/apps/{{ cookiecutter.app_slug }}/admin/__init__.py
    - src/apps/{{ cookiecutter.app_slug }}/admin/seeds.py
    - src/apps/{{ cookiecutter.app_slug }}/endpoints.py
    - src/apps/{{ cookiecutter.app_slug }}/messages.py
    - src/apps/{{ cookiecutter.app_slug }}/models.py
    - src/apps/{{ cookiecutter.app_slug }}/schemas.py
    - src/apps/{{ cookiecutter.app_slug }}/services.py

Next steps:
""")

for index, step in enumerate(steps):
    # Normalize indentation in the step text and remove trailing blank lines
    step_text = textwrap.dedent(step).rstrip()
    lines = step_text.splitlines()
    if lines:
        first, *rest = lines
    else:
        first, rest = "", []

    # Print the first line prefixed with the step number, then indent subsequent lines
    print(f"{index + 1} - {first}")
    for line in rest:
        print(line)
    print()

print("""----------------------------------------------------------------------
----------------------------------------------------------------------
----------------------------------------------------------------------""")