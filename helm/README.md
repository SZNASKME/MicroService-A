# 🚀 Helm Deployment Guide

## Prerequisites

- Kubernetes cluster (minikube, Docker Desktop, etc.)
- kubectl configured  
- **Helm 3.x installed**
- GitHub Personal Access Token with `read:packages` permission

## Install Helm

### Windows
```powershell
# Using Chocolatey
choco install kubernetes-helm

# Using Scoop
scoop install helm

# Using winget
winget install Helm.Helm
```

### Mac
```bash
# Using Homebrew
brew install helm
```

### Linux
```bash
# Using package manager
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

## Chart Structure

```
helm/
├── microservice-a/
│   ├── Chart.yaml                 # Chart metadata
│   ├── values.yaml               # Default values
│   └── templates/
│       ├── deployment.yaml       # Deployment template
│       ├── service.yaml          # Service template
│       ├── configmap.yaml        # ConfigMap template
│       ├── hpa.yaml              # HPA template
│       ├── ingress.yaml          # Ingress template
│       └── _helpers.tpl          # Template helpers
└── environments/
    ├── development.yaml          # Development values
    └── production.yaml           # Production values
```

## Quick Start

### 1. Set GitHub Token
```bash
# Windows
set GITHUB_TOKEN=ghp_your_token_here

# Linux/Mac
export GITHUB_TOKEN=ghp_your_token_here
```

### 2. Deploy

#### Development Environment
```bash
# Windows
helm-deploy.bat development

# Linux/Mac
chmod +x helm-deploy.sh
./helm-deploy.sh development
```

#### Production Environment
```bash
# Windows
helm-deploy.bat production

# Linux/Mac
./helm-deploy.sh production
```

## Manual Helm Commands

### Install/Upgrade
```bash
# Development
helm upgrade --install microservice-a helm/microservice-a \
  --values helm/environments/development.yaml \
  --wait --timeout=300s

# Production
helm upgrade --install microservice-a helm/microservice-a \
  --values helm/environments/production.yaml \
  --wait --timeout=300s
```

### Manage Releases
```bash
# List releases
helm list

# Get release status
helm status microservice-a

# Get release values
helm get values microservice-a

# Rollback
helm rollback microservice-a 1

# Uninstall
helm uninstall microservice-a
```

### Template Validation
```bash
# Dry run
helm install microservice-a helm/microservice-a --dry-run --debug

# Template rendering
helm template microservice-a helm/microservice-a

# With custom values
helm template microservice-a helm/microservice-a \
  --values helm/environments/production.yaml
```

## Configuration

### Environment-specific Values

#### Development (`helm/environments/development.yaml`)
- Single replica
- Debug logging
- NodePort on 30001
- Lower resource limits
- No autoscaling

#### Production (`helm/environments/production.yaml`)
- Multiple replicas (5)
- Production logging
- Ingress enabled
- Higher resource limits
- Autoscaling enabled

### Custom Values
```bash
# Override specific values
helm upgrade --install microservice-a helm/microservice-a \
  --set replicaCount=5 \
  --set image.tag=v2.0.0 \
  --set resources.limits.memory=1Gi
```

### Values File
```yaml
# custom-values.yaml
replicaCount: 3
image:
  tag: custom-tag
ingress:
  enabled: true
  hosts:
    - host: my-api.example.com
```

```bash
helm upgrade --install microservice-a helm/microservice-a \
  --values custom-values.yaml
```

## Monitoring & Troubleshooting

### Check Status
```bash
# Helm release status
helm status microservice-a

# Kubernetes resources
kubectl get all -l app.kubernetes.io/name=microservice-a

# Logs
kubectl logs -l app.kubernetes.io/name=microservice-a -f
```

### Debug
```bash
# Render templates without installing
helm template microservice-a helm/microservice-a --debug

# Install with debug output
helm install microservice-a helm/microservice-a --debug --dry-run
```

## Access Points

### Development
- **Application:** http://localhost:30001
- **Health Check:** http://localhost:30001/health
- **Metrics:** http://localhost:30001/metrics

### Production
- **Ingress:** https://api.yourdomain.com
- **Health Check:** https://api.yourdomain.com/health
- **Metrics:** https://api.yourdomain.com/metrics

## Cleanup

```bash
# Uninstall Helm release
helm uninstall microservice-a

# Delete namespace (if created)
kubectl delete namespace microservice-a

# Delete secrets
kubectl delete secret ghcr-secret
```
