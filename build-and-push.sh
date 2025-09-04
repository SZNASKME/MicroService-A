#!/bin/bash
# build-and-push.sh - Build and push Docker image to GHCR

set -e

# Configuration
REPO_URL="https://github.com/sznaskme/MicroService-A.git"
IMAGE_NAME="ghcr.io/sznaskme/microservice-a/orders"
VERSION_TAG="${1:-latest}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

log_step "🏗️ Building and pushing MicroService-A image..."
log_info "Target image: ${IMAGE_NAME}:${VERSION_TAG}"

# Check prerequisites
log_step "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed"
    exit 1
fi

if ! command -v git &> /dev/null; then
    log_error "Git is not installed"
    exit 1
fi

if [[ -z "${GITHUB_TOKEN}" ]]; then
    log_error "GITHUB_TOKEN environment variable is not set"
    log_info "Please run: export GITHUB_TOKEN=ghp_your_token_here"
    exit 1
fi

# Check Docker daemon
if ! docker info &> /dev/null; then
    log_error "Docker daemon is not running"
    log_info "Please start Docker service: sudo systemctl start docker"
    exit 1
fi

log_info "Prerequisites check passed ✅"

# Login to GHCR
log_step "🔑 Logging into GitHub Container Registry..."
if echo "$GITHUB_TOKEN" | docker login ghcr.io -u sznaskme --password-stdin; then
    log_info "GHCR login successful ✅"
else
    log_error "GHCR login failed"
    exit 1
fi

# Clone or update repository
if [[ ! -d "MicroService-A" ]]; then
    log_step "📥 Cloning repository..."
    if git clone "$REPO_URL"; then
        log_info "Repository cloned successfully ✅"
    else
        log_error "Failed to clone repository"
        exit 1
    fi
else
    log_step "📥 Updating repository..."
    cd MicroService-A
    if git pull; then
        log_info "Repository updated successfully ✅"
    else
        log_warn "Failed to update repository, continuing with current version"
    fi
    cd ..
fi

# Navigate to application directory
cd MicroService-A/services/orders

# Verify Dockerfile exists
if [[ ! -f "Dockerfile" ]]; then
    log_error "Dockerfile not found in services/orders/"
    exit 1
fi

# Create buildx builder if not exists
log_step "🔧 Setting up Docker buildx..."
if ! docker buildx ls | grep -q "multiarch-builder"; then
    docker buildx create --use --name multiarch-builder
    log_info "Created new buildx builder: multiarch-builder"
else
    docker buildx use multiarch-builder
    log_info "Using existing buildx builder: multiarch-builder"
fi

# Build and push image
log_step "🚀 Building Docker image..."
log_info "Building for platforms: linux/amd64, linux/arm64"

BUILD_ARGS=(
    --platform linux/amd64,linux/arm64
    --tag "${IMAGE_NAME}:latest"
    --tag "${IMAGE_NAME}:${VERSION_TAG}"
    --push
    .
)

if docker buildx build "${BUILD_ARGS[@]}"; then
    log_info "Build and push completed successfully ✅"
else
    log_error "Build and push failed"
    exit 1
fi

# Verify image was pushed
log_step "🔍 Verifying image was pushed..."
if docker manifest inspect "${IMAGE_NAME}:${VERSION_TAG}" &> /dev/null; then
    log_info "Image verification successful ✅"
else
    log_warn "Could not verify image (this might be normal)"
fi

# Cleanup
log_step "🧹 Cleaning up..."
cd ../../..

log_info ""
log_info "✅ Build and push completed successfully!"
log_info "📦 Image: ${IMAGE_NAME}:${VERSION_TAG}"
log_info "🌐 Available at: https://github.com/sznaskme/MicroService-A/pkgs/container/microservice-a%2Forders"
log_info ""
log_info "Next steps:"
log_info "1. Switch to deploy machine"
log_info "2. Set GITHUB_TOKEN environment variable"
log_info "3. Run: ./production-deploy.sh production default ${VERSION_TAG}"
