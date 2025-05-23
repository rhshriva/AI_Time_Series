#!/bin/bash
# Script to generate a Dockerfile for AI_Time_Series project
# Usage: ./scripts/create_dockerfile.sh

set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
DOCKERFILE_PATH="$PROJECT_ROOT/scripts/Dockerfile"

cat > "$DOCKERFILE_PATH" <<EOF
# AI_Time_Series Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "gpu_metrics_collector.py"]
EOF

echo "Dockerfile created at $DOCKERFILE_PATH"
