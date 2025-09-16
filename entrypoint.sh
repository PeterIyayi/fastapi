#!/bin/bash
set -e

# Load environment variables from .env
export $(grep -v '^#' /app/.env | xargs)

# Start FastAPI in the background
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Wait a moment to ensure FastAPI is up
sleep 2

# Start ngrok with your reserved domain
ngrok http 8000 --authtoken="$NGROK_AUTHTOKEN" --region=us --domain=scratchably-unfooling-christiane.ngrok-free.app --log=stdout
