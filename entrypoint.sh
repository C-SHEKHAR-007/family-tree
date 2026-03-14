#!/bin/sh

echo "Waiting for database..."

sleep 5

echo "Running migrations..."
alembic upgrade head || exit 1

echo "Starting FastAPI server..."

uvicorn app.main:app --host 0.0.0.0 --port 8000