#!/bin/bash
# Optimized Docker build script for production

set -e

# Configuration
IMAGE_NAME="ghcr.io/sznaskme/microservice-a/orders"
VERSION=${1:-latest}
DOCKERFILE_PATH="services/orders/Dockerfile"
BUILD_CONTEXT="services/orders"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validate environment
if [ ! -f "${DOCKERFILE_PATH}" ]; then
    log_error "Dockerfile not found at ${DOCKERFILE_PATH}"
    exit 1
fi

if [ ! -f "${BUILD_CONTEXT}/requirements.txt" ]; then
    log_error "requirements.txt not found in ${BUILD_CONTEXT}"
    exit 1
fi

log_info "Starting optimized Docker build..."
log_info "Image: ${IMAGE_NAME}:${VERSION}"
log_info "Context: ${BUILD_CONTEXT}"

# Create buildx builder if not exists
log_info "Setting up buildx builder..."
docker buildx create --name microservice-builder --use 2>/dev/null || true

# Build multi-platform image
log_info "Building multi-platform image..."
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --cache-from type=registry,ref=${IMAGE_NAME}:cache \
    --cache-to type=registry,ref=${IMAGE_NAME}:cache,mode=max \
    -f ${DOCKERFILE_PATH} \
    -t ${IMAGE_NAME}:${VERSION} \
    -t ${IMAGE_NAME}:latest \
    --push \
    ${BUILD_CONTEXT}

if [ $? -eq 0 ]; then
    log_info "✅ Build completed successfully!"
    log_info "Images pushed:"
    log_info "  - ${IMAGE_NAME}:${VERSION}"
    log_info "  - ${IMAGE_NAME}:latest"
else
    log_error "❌ Build failed!"
    exit 1
fi
