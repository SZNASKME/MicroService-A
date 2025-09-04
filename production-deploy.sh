#!/bin/bash
# production-deploy.sh - Deploy to Kubernetes using Helm

set -e

# Configuration
CHART_PATH="./helm/microservice-a"
IMAGE_NAME="ghcr.io/sznaskme/microservice-a/orders"

# Default values
ENVIRONMENT="${1:-development}"
NAMESPACE="${2:-default}"
VERSION_TAG="${3:-latest}"
RELEASE_NAME="microservice-a-$ENVIRONMENT"

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

log_step "🚀 Deploying MicroService-A to Kubernetes..."
log_info "Environment: $ENVIRONMENT"
log_info "Namespace: $NAMESPACE"
log_info "Version: $VERSION_TAG"
log_info "Release: $RELEASE_NAME"

# Check prerequisites
log_step "Checking prerequisites..."

if ! command -v helm &> /dev/null; then
    log_error "Helm is not installed"
    log_info "Install Helm: https://helm.sh/docs/intro/install/"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    log_error "kubectl is not installed"
    log_info "Install kubectl: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Check kubectl connection
if ! kubectl cluster-info &> /dev/null; then
    log_error "Cannot connect to Kubernetes cluster"
    log_info "Please check your kubeconfig or cluster connection"
    exit 1
fi

# Check Helm chart exists
if [[ ! -d "$CHART_PATH" ]]; then
    log_error "Helm chart not found at: $CHART_PATH"
    log_info "Please ensure you're in the repository root directory"
    exit 1
fi

# Check environment values file
ENV_VALUES_FILE="./helm/environments/${ENVIRONMENT}.yaml"
if [[ ! -f "$ENV_VALUES_FILE" ]]; then
    log_error "Environment values file not found: $ENV_VALUES_FILE"
    log_info "Available environments: development, production"
    exit 1
fi

log_info "Prerequisites check passed ✅"

# Create namespace if it doesn't exist
log_step "📁 Preparing namespace..."
if kubectl get namespace "$NAMESPACE" &> /dev/null; then
    log_info "Namespace '$NAMESPACE' already exists"
else
    log_info "Creating namespace '$NAMESPACE'"
    kubectl create namespace "$NAMESPACE"
fi

# Setup GHCR access if token is provided
if [[ -n "${GITHUB_TOKEN}" ]]; then
    log_step "🔑 Setting up GHCR access..."
    
    SECRET_NAME="ghcr-secret"
    
    # Delete existing secret if it exists
    kubectl delete secret "$SECRET_NAME" -n "$NAMESPACE" 2>/dev/null || true
    
    # Create new secret
    kubectl create secret docker-registry "$SECRET_NAME" \
        --docker-server=ghcr.io \
        --docker-username=sznaskme \
        --docker-password="$GITHUB_TOKEN" \
        --namespace="$NAMESPACE"
    
    log_info "GHCR access configured ✅"
else
    log_warn "GITHUB_TOKEN not set - using public access"
fi

# Validate Helm chart
log_step "✅ Validating Helm chart..."
if helm lint "$CHART_PATH"; then
    log_info "Helm chart validation passed ✅"
else
    log_error "Helm chart validation failed"
    exit 1
fi

# Check if image exists and is accessible
log_step "🔍 Checking image availability..."
IMAGE_FULL="${IMAGE_NAME}:${VERSION_TAG}"

if kubectl run test-image-access \
    --image="$IMAGE_FULL" \
    --dry-run=client \
    --output=yaml > /dev/null 2>&1; then
    log_info "Image access validation passed ✅"
else
    log_warn "Could not validate image access (might be normal)"
fi

# Perform dry-run deployment
log_step "🧪 Performing dry-run deployment..."
if helm upgrade "$RELEASE_NAME" "$CHART_PATH" \
    --install \
    --namespace "$NAMESPACE" \
    --values "$ENV_VALUES_FILE" \
    --set image.tag="$VERSION_TAG" \
    --dry-run \
    --debug > /dev/null; then
    log_info "Dry-run deployment successful ✅"
else
    log_error "Dry-run deployment failed"
    exit 1
fi

# Deploy to Kubernetes
log_step "🚀 Deploying to Kubernetes..."
helm upgrade "$RELEASE_NAME" "$CHART_PATH" \
    --install \
    --namespace "$NAMESPACE" \
    --values "$ENV_VALUES_FILE" \
    --set image.tag="$VERSION_TAG" \
    --wait \
    --timeout=300s

if [[ $? -eq 0 ]]; then
    log_info "Deployment completed successfully ✅"
else
    log_error "Deployment failed"
    exit 1
fi

# Get deployment status
log_step "📊 Checking deployment status..."
echo ""
log_info "=== Deployment Status ==="
helm status "$RELEASE_NAME" -n "$NAMESPACE"

echo ""
log_info "=== Pod Status ==="
kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/name=microservice-a

echo ""
log_info "=== Service Status ==="
kubectl get services -n "$NAMESPACE" -l app.kubernetes.io/name=microservice-a

# Health check
log_step "🏥 Performing health check..."
sleep 10

POD_NAME=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/name=microservice-a -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [[ -n "$POD_NAME" ]]; then
    log_info "Testing health endpoint..."
    if kubectl exec -n "$NAMESPACE" "$POD_NAME" -- curl -s http://localhost:5000/health > /dev/null 2>&1; then
        log_info "Health check passed ✅"
    else
        log_warn "Health check failed - application might still be starting"
    fi
else
    log_warn "No pods found - checking deployment..."
fi

# Show access information
echo ""
log_info "=== Access Information ==="
SERVICE_NAME=$(kubectl get services -n "$NAMESPACE" -l app.kubernetes.io/name=microservice-a -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [[ -n "$SERVICE_NAME" ]]; then
    SERVICE_TYPE=$(kubectl get service "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.type}')
    SERVICE_PORT=$(kubectl get service "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].port}')
    
    log_info "Service: $SERVICE_NAME"
    log_info "Type: $SERVICE_TYPE"
    log_info "Port: $SERVICE_PORT"
    
    if [[ "$SERVICE_TYPE" == "LoadBalancer" ]]; then
        EXTERNAL_IP=$(kubectl get service "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
        if [[ -n "$EXTERNAL_IP" ]]; then
            log_info "External IP: $EXTERNAL_IP"
            log_info "Application URL: http://$EXTERNAL_IP:$SERVICE_PORT"
        else
            log_info "External IP: <pending>"
        fi
    elif [[ "$SERVICE_TYPE" == "NodePort" ]]; then
        NODE_PORT=$(kubectl get service "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].nodePort}')
        log_info "NodePort: $NODE_PORT"
        log_info "Access via: http://<node-ip>:$NODE_PORT"
    else
        log_info "Use port-forward: kubectl port-forward -n $NAMESPACE service/$SERVICE_NAME 8080:$SERVICE_PORT"
    fi
fi

echo ""
log_info "✅ Deployment completed successfully!"
log_info "🎉 MicroService-A is now running in Kubernetes"
log_info ""
log_info "Useful commands:"
log_info "  View logs: kubectl logs -n $NAMESPACE -l app.kubernetes.io/name=microservice-a -f"
log_info "  Scale app: kubectl scale deployment -n $NAMESPACE $RELEASE_NAME --replicas=3"
log_info "  Port forward: kubectl port-forward -n $NAMESPACE service/$SERVICE_NAME 8080:$SERVICE_PORT"
log_info "  Rollback: helm rollback $RELEASE_NAME -n $NAMESPACE"
