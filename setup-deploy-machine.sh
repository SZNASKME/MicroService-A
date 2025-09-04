#!/bin/bash
# setup-deploy-machine.sh - Quick setup for deploy machine

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

log_step "🚀 Setting up Deploy Machine for MicroService-A..."

# Update system
log_step "📦 Updating system packages..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y curl wget git ca-certificates
elif command -v yum &> /dev/null; then
    sudo yum update -y
    sudo yum install -y curl wget git ca-certificates
else
    log_error "Unsupported package manager. Please install manually."
    exit 1
fi

# Install kubectl if not present
if ! command -v kubectl &> /dev/null; then
    log_step "⚙️ Installing kubectl..."
    
    # Download kubectl
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    
    # Validate binary
    curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
    echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
    
    # Install kubectl
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl kubectl.sha256
    
    log_info "kubectl installed successfully ✅"
else
    log_info "kubectl is already installed ✅"
fi

# Install Helm if not present
if ! command -v helm &> /dev/null; then
    log_step "⛵ Installing Helm..."
    
    # Download and install Helm
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    
    log_info "Helm installed successfully ✅"
else
    log_info "Helm is already installed ✅"
fi

# Verify installations
log_step "🔍 Verifying installations..."
kubectl version --client
helm version

# Create deploy directory
DEPLOY_DIR="$HOME/microservice-deploy"
log_step "📁 Creating deploy directory: $DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

# Clone repository for Helm charts
log_step "📥 Cloning repository for Helm charts..."
if [[ ! -d "MicroService-A" ]]; then
    git clone https://github.com/sznaskme/MicroService-A.git
else
    cd MicroService-A
    git pull
    cd ..
fi

# Copy deploy script
log_step "📋 Setting up deploy script..."
cp MicroService-A/production-deploy.sh .
chmod +x production-deploy.sh

log_info "Setup completed successfully ✅"
echo ""
log_info "=== Next Steps ==="
log_info "1. Configure kubectl to connect to your Kubernetes cluster:"
log_info "   - For managed clusters (EKS, GKE, AKS): Use cloud provider CLI"
log_info "   - For custom clusters: Copy kubeconfig file"
log_info ""
log_info "2. Test kubectl connection:"
log_info "   kubectl cluster-info"
log_info "   kubectl get nodes"
log_info ""
log_info "3. (Optional) Set GitHub token for private registry:"
log_info "   export GITHUB_TOKEN=ghp_your_token_here"
log_info ""
log_info "4. Deploy the application:"
log_info "   cd $DEPLOY_DIR"
log_info "   ./production-deploy.sh [environment] [namespace] [version]"
log_info ""
log_info "Examples:"
log_info "   ./production-deploy.sh development default latest"
log_info "   ./production-deploy.sh production prod-ns v1.0.0"
echo ""
log_info "=== Kubernetes Configuration Examples ==="
echo ""
log_info "For EKS (AWS):"
log_info "   aws eks update-kubeconfig --region us-west-2 --name my-cluster"
echo ""
log_info "For GKE (Google Cloud):"
log_info "   gcloud container clusters get-credentials my-cluster --zone=us-central1-a"
echo ""
log_info "For AKS (Azure):"
log_info "   az aks get-credentials --resource-group myResourceGroup --name myCluster"
echo ""
log_info "For custom cluster:"
log_info "   export KUBECONFIG=/path/to/kubeconfig"
