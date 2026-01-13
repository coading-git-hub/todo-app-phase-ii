#!/usr/bin/env bash
set -e  # Exit on any error

echo "Starting backend installation and setup..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Dependencies installed successfully"

# Run any pending database migrations
# python -m alembic upgrade head

echo "Starting FastAPI application..."
# Start the FastAPI application with uvicorn
exec uvicorn src.main:app --host 0.0.0.0 --port $PORT