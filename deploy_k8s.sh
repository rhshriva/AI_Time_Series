#!/bin/bash
# Root-level script to build Docker image and deploy to Kubernetes using scripts/deploy_k8s.sh

set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/scripts" && pwd)"

# Pass optional image tag as argument
bash "$SCRIPTS_DIR/deploy_k8s.sh" "$@"
