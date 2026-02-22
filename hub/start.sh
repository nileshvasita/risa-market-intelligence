#!/bin/bash
cd "$(dirname "$0")"
echo "🔨 Building database..."
python3 build_db.py
echo ""
echo "🚀 Starting server on http://localhost:8501"
source .env 2>/dev/null  # Load ANTHROPIC_API_KEY from .env
uvicorn server:app --host 0.0.0.0 --port 8501
