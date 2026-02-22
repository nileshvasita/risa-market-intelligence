#!/bin/bash
cd "$(dirname "$0")"
source .env 2>/dev/null
echo "🔨 Building database..."
python3 build_db.py
echo ""
echo "🚀 Starting server on http://localhost:8501"
uvicorn server:app --host 0.0.0.0 --port 8501
