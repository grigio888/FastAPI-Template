# Use python docker image from global DockerHub as base image
FROM python:3.13-alpine AS base

# Define a new stage build based on the base image
FROM base AS build

# Set the working directory in the image to /app. All subsequent instructions are relative to this path.
WORKDIR  /app

# Copy the application's pyproject.toml and poetry.lock (if exists) to the working directory
# and copy the necessary files for package creation.
COPY ./pyproject.toml /app/
COPY ./README.md /app/

# Install poetry, create a virtual environment in the project directory, configure poetry and install project dependencies
# Setting virtualenvs.in-project true makes poetry create the virtual environment in the project's root directory
# poetry install without arguments reads the pyproject.toml file from the current project and installs the dependencies specified
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install


# Define a new stage based on the base image
FROM base

# Define default environment variables
ENV APP_NAME="Template"

# Set system environments for Python to ensure smooth running
# PYTHONUNBUFFERED=1 ensures that Python output is logged to the terminal where it can be consumed by logging utilities
# PYTHONDONTWRITEBYTECODE=1 ensures that Python does not try to write .pyc files which we do not need in this case
# PYTHONPATH and PATH variables are set to include the .venv directory
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/.venv/lib/python3.13/site-packages" \
    PATH="/app/.venv/bin:$PATH"

# Set the working directory in this stage to /app
WORKDIR /app

# Copy the virtual environment .venv from the build stage to the current stage
COPY --from=build /app/.venv .venv

# Copy env/dev/scripts from the project to the Docker image
COPY ./alembic.ini ./alembic.ini
COPY ./env/dev/entrypoint.sh scripts/entrypoint.sh

# Copy application code to the Docker image
COPY src ./src

# Define the command to run the application using bash
# The script entrypoint.sh is expected to start the application
ENTRYPOINT ["sh", "./scripts/entrypoint.sh"]
