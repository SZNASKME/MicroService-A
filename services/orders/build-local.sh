#!/bin/bash
# Local build script for testing

set -e

echo "🧪 Building local test image..."

# Navigate to project root
cd "$(dirname "$0")/../.."

# Build locally
docker build \
    -f services/orders/Dockerfile \
    -t microservice-a-orders:local \
    services/orders

echo "✅ Local build completed!"
echo "Run with: docker run -p 5000:5000 microservice-a-orders:local"
