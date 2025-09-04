# 🚀 Complete Build & Deploy Guide

## 📋 Repository Structure Validation

```
MicroService-A/
├── services/orders/           ✅ Application Source
│   ├── app.py                ✅ Flask Application
│   ├── wsgi.py               ✅ WSGI Entry Point
│   ├── config.py             ✅ Configuration
│   ├── requirements.txt      ✅ Dependencies
│   ├── Dockerfile            ✅ Container Build
│   ├── .dockerignore         ✅ Docker Ignore
│   ├── .env.production       ✅ Production Config
│   └── features/             ✅ Analytics Service
│       ├── __init__.py
│       └── analytics_service.py
├── helm/                     ✅ Helm Chart
│   ├── microservice-a/       ✅ Chart Definition
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   ├── .helmignore
│   │   └── templates/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── configmap.yaml
│   │       ├── hpa.yaml
│   │       ├── ingress.yaml
│   │       └── _helpers.tpl
│   ├── environments/         ✅ Environment Configs
│   │   ├── development.yaml
│   │   └── production.yaml
│   └── README.md
├── helm-deploy.sh            ✅ Helm Deploy Script
├── helm-deploy.bat           ✅ Windows Deploy Script
├── k8s-all-in-one.yaml      ✅ Fallback YAML
└── DEPLOY-README.md          ✅ Documentation
```

---

## 🏗️ BUILD PROCESS (Linux Build Machine)

### Machine A: Build & Push Image

#### 1. Prerequisites
```bash
# Install required tools
sudo apt update
sudo apt install -y git docker.io

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (logout/login required)
sudo usermod -aG docker $USER
```

#### 2. Clone Repository
```bash
# Clone the repository
git clone https://github.com/sznaskme/MicroService-A.git
cd MicroService-A

# Verify structure
tree -a services/orders/
```

#### 3. Setup GitHub Container Registry
```bash
# Set GitHub Personal Access Token
export GITHUB_TOKEN="ghp_your_github_token_here"

# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u sznaskme --password-stdin
```

#### 4. Build Docker Image
```bash
# Navigate to application directory
cd services/orders

# Build multi-platform image
docker buildx create --use --name multiarch-builder
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag ghcr.io/sznaskme/microservice-a/orders:latest \
  --tag ghcr.io/sznaskme/microservice-a/orders:v1.0.0 \
  --push \
  .

# Verify image
docker images | grep microservice-a
```

#### 5. Build Script for Automation
```bash
#!/bin/bash
# build-and-push.sh

set -e

# Configuration
REPO_URL="https://github.com/sznaskme/MicroService-A.git"
IMAGE_NAME="ghcr.io/sznaskme/microservice-a/orders"
VERSION_TAG="${1:-latest}"

echo "🏗️ Building and pushing MicroService-A image..."

# Check prerequisites
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

if [[ -z "${GITHUB_TOKEN}" ]]; then
    echo "❌ GITHUB_TOKEN environment variable is not set"
    exit 1
fi

# Login to GHCR
echo "🔑 Logging into GitHub Container Registry..."
echo $GITHUB_TOKEN | docker login ghcr.io -u sznaskme --password-stdin

# Clone or update repository
if [[ ! -d "MicroService-A" ]]; then
    echo "📥 Cloning repository..."
    git clone "$REPO_URL"
else
    echo "📥 Updating repository..."
    cd MicroService-A && git pull && cd ..
fi

# Build and push image
echo "🚀 Building Docker image..."
cd MicroService-A/services/orders

# Create buildx builder if not exists
docker buildx create --use --name multiarch-builder 2>/dev/null || docker buildx use multiarch-builder

# Build and push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag "${IMAGE_NAME}:latest" \
  --tag "${IMAGE_NAME}:${VERSION_TAG}" \
  --push \
  .

echo "✅ Build and push completed!"
echo "Image: ${IMAGE_NAME}:${VERSION_TAG}"
```

#### 6. Usage
```bash
# Make script executable
chmod +x build-and-push.sh

# Build with latest tag
export GITHUB_TOKEN="ghp_your_token_here"
./build-and-push.sh

# Build with specific version
./build-and-push.sh v1.0.1
```

---

## 🚀 DEPLOY PROCESS (Linux Deploy Machine)

### Machine B: Deploy to Kubernetes

#### 1. Prerequisites
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://get.helm.sh/helm-v3.12.0-linux-amd64.tar.gz | tar -xz
sudo mv linux-amd64/helm /usr/local/bin/

# Verify installations
kubectl version --client
helm version
```

#### 2. Setup Kubernetes Cluster
```bash
# For minikube (development)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start

# For existing cluster, configure kubectl
# kubectl config use-context your-cluster-context
```

#### 3. Clone Repository (Deploy Machine)
```bash
# Clone repository
git clone https://github.com/sznaskme/MicroService-A.git
cd MicroService-A

# Verify Helm chart
helm lint helm/microservice-a
```

#### 4. Setup GitHub Container Registry Access
```bash
# Set GitHub token
export GITHUB_TOKEN="ghp_your_github_token_here"

# Create GHCR secret in Kubernetes
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=sznaskme \
  --docker-password="${GITHUB_TOKEN}" \
  --namespace=default
```

#### 5. Deploy with Helm
```bash
# Development deployment
chmod +x helm-deploy.sh
./helm-deploy.sh development

# Production deployment
./helm-deploy.sh production

# Custom deployment with overrides
helm upgrade --install microservice-a helm/microservice-a \
  --namespace default \
  --values helm/environments/production.yaml \
  --set image.tag=v1.0.1 \
  --set replicaCount=5 \
  --wait --timeout=600s
```

#### 6. Deploy Script for Production
```bash
#!/bin/bash
# production-deploy.sh

set -e

# Configuration
ENVIRONMENT="${1:-production}"
RELEASE_NAME="microservice-a"
NAMESPACE="${2:-default}"
IMAGE_TAG="${3:-latest}"

echo "🚀 Deploying MicroService-A to $ENVIRONMENT..."

# Prerequisites check
if ! command -v helm &> /dev/null; then
    echo "❌ Helm is not installed"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed"
    exit 1
fi

if [[ -z "${GITHUB_TOKEN}" ]]; then
    echo "❌ GITHUB_TOKEN environment variable is not set"
    exit 1
fi

# Check cluster connectivity
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster"
    exit 1
fi

# Create namespace if not exists
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Create/update GHCR secret
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=sznaskme \
  --docker-password="${GITHUB_TOKEN}" \
  --namespace="$NAMESPACE" \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy with Helm
echo "🚀 Deploying with Helm..."
VALUES_FILE="helm/environments/${ENVIRONMENT}.yaml"

if [[ -f "$VALUES_FILE" ]]; then
    helm upgrade --install "$RELEASE_NAME" helm/microservice-a \
      --namespace "$NAMESPACE" \
      --values "$VALUES_FILE" \
      --set image.tag="$IMAGE_TAG" \
      --wait --timeout=600s
else
    echo "❌ Values file not found: $VALUES_FILE"
    exit 1
fi

# Verify deployment
echo "✅ Deployment completed! Checking status..."
kubectl get pods -l app.kubernetes.io/name=microservice-a -n "$NAMESPACE"
kubectl get svc -l app.kubernetes.io/name=microservice-a -n "$NAMESPACE"

echo "📊 Helm release info:"
helm status "$RELEASE_NAME" -n "$NAMESPACE"

echo "🎉 Deployment successful!"
```

#### 7. Usage Examples
```bash
# Basic production deployment
export GITHUB_TOKEN="ghp_your_token_here"
chmod +x production-deploy.sh
./production-deploy.sh production

# Deploy specific version to custom namespace
./production-deploy.sh production microservice-prod v1.0.1

# Development deployment
./production-deploy.sh development
```

---

## 🔄 COMPLETE CI/CD WORKFLOW

### Build Machine (Machine A)
```bash
# 1. Setup
export GITHUB_TOKEN="ghp_your_token_here"

# 2. Build and push latest
./build-and-push.sh

# 3. Build and push versioned
./build-and-push.sh v1.0.1
```

### Deploy Machine (Machine B)
```bash
# 1. Setup
export GITHUB_TOKEN="ghp_your_token_here"

# 2. Deploy development (for testing)
./production-deploy.sh development

# 3. Deploy production
./production-deploy.sh production default v1.0.1
```

---

## 🌐 ACCESS & VERIFICATION

### After Deployment
```bash
# Check deployment status
kubectl get pods -l app.kubernetes.io/name=microservice-a
kubectl get svc -l app.kubernetes.io/name=microservice-a

# Get service URLs
kubectl get svc microservice-a-nodeport -o jsonpath='{.spec.ports[0].nodePort}'

# Test application
curl http://localhost:30000/health
curl http://localhost:30000/metrics

# View logs
kubectl logs -l app.kubernetes.io/name=microservice-a -f

# Scale application
helm upgrade microservice-a helm/microservice-a --set replicaCount=5
```

---

## 🛠️ TROUBLESHOOTING

### Common Issues
```bash
# Image pull errors
kubectl describe pod <pod-name> | grep -A5 "Failed"
kubectl get secret ghcr-secret -o yaml

# Helm issues
helm lint helm/microservice-a
helm template microservice-a helm/microservice-a --debug

# Connectivity issues
kubectl cluster-info
kubectl get nodes
```

### Rollback
```bash
# Helm rollback
helm history microservice-a
helm rollback microservice-a 1

# Force pod restart
kubectl rollout restart deployment/microservice-a
```

---

## 📋 SUMMARY

### Build Machine Requirements
- ✅ Docker with buildx
- ✅ Git
- ✅ GitHub token with packages:write
- ✅ Internet access to GHCR

### Deploy Machine Requirements  
- ✅ kubectl configured
- ✅ Helm 3.x
- ✅ Kubernetes cluster access
- ✅ GitHub token with packages:read
- ✅ Repository access

### Key Files for Deploy Machine
- ✅ `helm/` directory (complete chart)
- ✅ `helm-deploy.sh` or `production-deploy.sh`
- ✅ GitHub token for GHCR access

**This setup provides a complete separation of build and deploy processes with proper security and automation!** 🎉
