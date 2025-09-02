#!/bin/bash
# Production build script

set -e

# Configuration
IMAGE_REPO="${IMAGE_REPO:-ghcr.io/sznaskme/microservice-a/orders}"
VERSION="${1:-latest}"
DOCKER_PACKAGE_NAME="${DOCKER_PACKAGE_NAME:-microservice-a-builder}"

echo "🚀 Building production image..."
echo "Image: ${IMAGE_REPO}:${VERSION}"

# Navigate to correct directory
cd "$(dirname "$0")"

# Verify files exist
if [ ! -f "services/orders/Dockerfile" ]; then
    echo "❌ Error: Dockerfile not found at services/orders/Dockerfile"
    exit 1
fi

if [ ! -f "services/orders/requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found at services/orders/requirements.txt"
    exit 1
fi

# Create builder (ignore if exists)
echo "📦 Setting up buildx builder..."
docker buildx create --name ${DOCKER_PACKAGE_NAME} >/dev/null 2>&1 || true
docker buildx use ${DOCKER_PACKAGE_NAME}

# Build and push
echo "🔨 Building multi-platform image..."
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --cache-from type=registry,ref=${IMAGE_REPO}:cache \
    --cache-to type=registry,ref=${IMAGE_REPO}:cache,mode=max \
    -t ${IMAGE_REPO}:${VERSION} \
    -t ${IMAGE_REPO}:latest \
    -f services/orders/Dockerfile \
    services/orders \
    --push

echo "✅ Build completed successfully!"
echo "Images pushed:"
echo "  - ${IMAGE_REPO}:${VERSION}"
echo "  - ${IMAGE_REPO}:latest"
