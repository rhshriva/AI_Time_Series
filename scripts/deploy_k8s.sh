#!/bin/bash
# Script to build Docker image and deploy to Kubernetes
# Usage: ./scripts/deploy_k8s.sh <image_tag>

set -e

IMAGE_TAG=${1:-ai-gpu-metrics-collector:latest}
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKERFILE_PATH="$PROJECT_ROOT/scripts/Dockerfile"
DEPLOYMENT_DIR="$PROJECT_ROOT/deployment"

# Build Docker image

echo "Building Docker image: $IMAGE_TAG"
docker build -t $IMAGE_TAG -f "$DOCKERFILE_PATH" "$PROJECT_ROOT"

echo "Docker image $IMAGE_TAG built successfully."

echo "Applying Kubernetes manifests from $DEPLOYMENT_DIR..."
kubectl apply -f "$DEPLOYMENT_DIR/metrics-collector-configmap.yaml"
kubectl apply -f "$DEPLOYMENT_DIR/metrics-collector-deployment.yaml"

echo "Deployment to Kubernetes complete."
