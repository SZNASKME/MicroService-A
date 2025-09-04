#!/bin/bash
# setup-build-machine.sh - Quick setup for build machine

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

log_step "🏗️ Setting up Build Machine for MicroService-A..."

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    log_warn "Running as root. Consider using a non-root user for Docker."
fi

# Update system
log_step "📦 Updating system packages..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y curl wget git ca-certificates gnupg lsb-release
elif command -v yum &> /dev/null; then
    sudo yum update -y
    sudo yum install -y curl wget git ca-certificates
else
    log_error "Unsupported package manager. Please install manually."
    exit 1
fi

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    log_step "🐳 Installing Docker..."
    
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y yum-utils
        sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin
    fi
    
    # Start and enable Docker
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    log_info "Docker installed successfully ✅"
    log_warn "Please log out and log back in to use Docker without sudo"
else
    log_info "Docker is already installed ✅"
fi

# Verify Docker installation
log_step "🔍 Verifying Docker installation..."
if sudo docker --version; then
    log_info "Docker version check passed ✅"
else
    log_error "Docker installation verification failed"
    exit 1
fi

# Enable buildx if not enabled
if ! docker buildx version &> /dev/null; then
    log_step "🔧 Setting up Docker Buildx..."
    docker buildx install
    log_info "Docker Buildx installed ✅"
else
    log_info "Docker Buildx is already available ✅"
fi

# Create build directory
BUILD_DIR="$HOME/microservice-build"
log_step "📁 Creating build directory: $BUILD_DIR"
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# Download build script
log_step "📥 Downloading build script..."
curl -fsSL https://raw.githubusercontent.com/sznaskme/MicroService-A/main/build-and-push.sh -o build-and-push.sh
chmod +x build-and-push.sh

log_info "Setup completed successfully ✅"
echo ""
log_info "=== Next Steps ==="
log_info "1. Get your GitHub Personal Access Token:"
log_info "   - Go to: https://github.com/settings/tokens"
log_info "   - Generate new token with 'write:packages' permission"
log_info ""
log_info "2. Set the token as environment variable:"
log_info "   export GITHUB_TOKEN=ghp_your_token_here"
log_info ""
log_info "3. Build and push the image:"
log_info "   cd $BUILD_DIR"
log_info "   ./build-and-push.sh [version-tag]"
log_info ""
log_info "Example:"
log_info "   export GITHUB_TOKEN=ghp_xxxxxxxxxxxx"
log_info "   ./build-and-push.sh v1.0.0"
echo ""
log_warn "Note: If you added user to docker group, please logout and login again"
