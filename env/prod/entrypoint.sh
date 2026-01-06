#!/bin/bash
echo "# ---------------------------------------------- #"
echo "#          $APP_NAME Entry Point Script          #"
echo "# ---------------------------------------------- #"

exec uvicorn src.main:app \
    --app-dir /app \
    --host ${HOST} \
    --port ${PORT} \
    --header server:HIDDEN;
