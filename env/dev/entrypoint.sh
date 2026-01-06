#!/bin/bash
echo Running Entrypoint.sh and starting app $APP_NAME

echo App $APP_NAME started as development
exec uvicorn src.main:app \
    --app-dir /app \
    --host ${HOST} \
    --port ${PORT} \
    --header server:HIDDEN;
