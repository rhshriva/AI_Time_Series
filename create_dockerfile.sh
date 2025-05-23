#!/bin/bash
# Root-level script to create Dockerfile using scripts/create_dockerfile.sh

set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/scripts" && pwd)"

bash "$SCRIPTS_DIR/create_dockerfile.sh"
