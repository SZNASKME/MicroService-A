# MicroService-A: Separated Build & Deploy Guide

Complete guide for building and deploying MicroService-A using separated Linux machines.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Build Machine  │    │  Container      │    │  Deploy Machine │
│     (Linux)     │────┤   Registry      ├────│     (Linux)     │
│                 │    │    (GHCR)       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
│                                                               │
├─ Docker Engine                                  ├─ kubectl    │
├─ Docker Buildx                                  ├─ Helm 3.x   │
├─ Git                                           ├─ Git        │
└─ GitHub Token                                   └─ Kubeconfig │
```

## 📋 Prerequisites

### Build Machine Requirements
- Linux (Ubuntu 20.04+, CentOS 8+, or similar)
- Docker Engine with Buildx support
- Git
- Internet connectivity
- GitHub Personal Access Token with `write:packages` permission

### Deploy Machine Requirements  
- Linux (Ubuntu 20.04+, CentOS 8+, or similar)
- kubectl configured with cluster access
- Helm 3.x
- Git
- Internet connectivity (to pull from GHCR)

### Kubernetes Cluster Requirements
- Kubernetes 1.20+
- Ingress controller (optional, for external access)
- Storage class for persistent volumes (if needed)

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Build Machine:**
```bash
curl -fsSL https://raw.githubusercontent.com/sznaskme/MicroService-A/main/setup-build-machine.sh | bash
export GITHUB_TOKEN=ghp_your_token_here
cd ~/microservice-build
./build-and-push.sh v1.0.0
```

**Deploy Machine:**
```bash
curl -fsSL https://raw.githubusercontent.com/sznaskme/MicroService-A/main/setup-deploy-machine.sh | bash
# Configure kubectl to connect to your cluster
cd ~/microservice-deploy
./production-deploy.sh production default v1.0.0
```

### Option 2: Manual Setup

Follow the detailed steps below for manual configuration.

## 🔧 Manual Setup Instructions

### Build Machine Setup

1. **Install Dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker.io docker-buildx git curl

# CentOS/RHEL
sudo yum install -y docker git curl
sudo systemctl start docker
sudo systemctl enable docker
```

2. **Configure Docker Access:**
```bash
sudo usermod -aG docker $USER
# Log out and log back in
```

3. **Get GitHub Token:**
   - Go to: https://github.com/settings/tokens
   - Generate new token with `write:packages` permission
   - Save token securely

4. **Download Build Scripts:**
```bash
mkdir ~/microservice-build && cd ~/microservice-build
wget https://raw.githubusercontent.com/sznaskme/MicroService-A/main/build-and-push.sh
chmod +x build-and-push.sh
```

### Deploy Machine Setup

1. **Install kubectl:**
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

2. **Install Helm:**
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

3. **Configure Kubernetes Access:**
```bash
# For managed clusters, use cloud provider CLI:
# AWS EKS:
aws eks update-kubeconfig --region us-west-2 --name my-cluster

# Google GKE:
gcloud container clusters get-credentials my-cluster --zone=us-central1-a

# Azure AKS:
az aks get-credentials --resource-group myResourceGroup --name myCluster

# For custom clusters, copy kubeconfig:
export KUBECONFIG=/path/to/kubeconfig
```

4. **Download Repository and Scripts:**
```bash
mkdir ~/microservice-deploy && cd ~/microservice-deploy
git clone https://github.com/sznaskme/MicroService-A.git
cp MicroService-A/production-deploy.sh .
chmod +x production-deploy.sh
```

## 🏗️ Build Process

### Standard Build
```bash
cd ~/microservice-build
export GITHUB_TOKEN=ghp_your_token_here
./build-and-push.sh latest
```

### Versioned Build
```bash
./build-and-push.sh v1.0.0
```

### Build Output
```
✅ Build and push completed successfully!
📦 Image: ghcr.io/sznaskme/microservice-a/orders:v1.0.0
🌐 Available at: https://github.com/sznaskme/MicroService-A/pkgs/container/microservice-a%2Forders
```

## 🚀 Deploy Process

### Development Deployment
```bash
cd ~/microservice-deploy
./production-deploy.sh development default latest
```

### Production Deployment
```bash
./production-deploy.sh production prod-ns v1.0.0
```

### Deploy Parameters
- **Environment:** `development` or `production`
- **Namespace:** Kubernetes namespace (created if not exists)
- **Version:** Docker image tag to deploy

## 📊 Monitoring and Management

### Check Deployment Status
```bash
# View pods
kubectl get pods -n production -l app.kubernetes.io/name=microservice-a

# View services
kubectl get services -n production

# View logs
kubectl logs -n production -l app.kubernetes.io/name=microservice-a -f

# Check health
kubectl port-forward -n production service/microservice-a-production 8080:80
curl http://localhost:8080/health
```

### Scaling
```bash
kubectl scale deployment -n production microservice-a-production --replicas=3
```

### Rollback
```bash
helm rollback microservice-a-production -n production
```

## 🔐 Security Best Practices

### Build Machine Security
- Use dedicated service account with minimal permissions
- Rotate GitHub tokens regularly
- Store tokens in secure credential management
- Run builds in isolated environment
- Enable Docker content trust

### Deploy Machine Security  
- Use RBAC for kubectl access
- Limit namespace permissions
- Store kubeconfig securely
- Enable audit logging
- Use network policies

### Container Security
- Images are scanned for vulnerabilities
- Non-root user execution
- Minimal base image (python:3.11-slim)
- No unnecessary packages
- Security contexts applied

## 🔄 CI/CD Integration

### GitHub Actions (Recommended)
See `.github/workflows/ci-cd.yml` for complete workflow that:
- Builds on every push/PR
- Deploys to development automatically
- Deploys to production on tag creation
- Includes security scanning and testing

### GitLab CI/CD
```yaml
# .gitlab-ci.yml
stages:
  - build
  - deploy

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA ./services/orders
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - helm upgrade microservice-a ./helm/microservice-a
        --install --namespace production
        --set image.tag=$CI_COMMIT_SHA
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh './build-and-push.sh ${BUILD_NUMBER}'
            }
        }
        
        stage('Deploy') {
            steps {
                sh './production-deploy.sh production default ${BUILD_NUMBER}'
            }
        }
    }
}
```

## 🐛 Troubleshooting

### Build Issues

**Docker permission denied:**
```bash
sudo usermod -aG docker $USER
# Log out and log back in
```

**GHCR authentication failed:**
```bash
# Verify token has write:packages permission
# Check token format: ghp_xxxxxxxxxxxx
echo $GITHUB_TOKEN | docker login ghcr.io -u sznaskme --password-stdin
```

**Buildx not available:**
```bash
docker buildx install
docker buildx create --use --name multiarch-builder
```

### Deploy Issues

**kubectl connection failed:**
```bash
kubectl cluster-info
kubectl config view
# Verify kubeconfig is correct
```

**Helm chart validation failed:**
```bash
helm lint ./helm/microservice-a
helm template test ./helm/microservice-a --values ./helm/environments/production.yaml
```

**Image pull failed:**
```bash
# Check if image exists
docker manifest inspect ghcr.io/sznaskme/microservice-a/orders:v1.0.0

# For private repos, ensure GITHUB_TOKEN is set during deploy
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=sznaskme \
  --docker-password=$GITHUB_TOKEN \
  --namespace=production
```

**Pod startup issues:**
```bash
kubectl describe pod -n production -l app.kubernetes.io/name=microservice-a
kubectl logs -n production -l app.kubernetes.io/name=microservice-a
```

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

## 💡 Tips for Production

1. **Use specific version tags** instead of `latest` in production
2. **Implement proper monitoring** with Prometheus and Grafana
3. **Set up log aggregation** with ELK or similar stack
4. **Configure backup strategies** for persistent data
5. **Test disaster recovery procedures** regularly
6. **Monitor resource usage** and set appropriate limits
7. **Implement security scanning** in your CI/CD pipeline
8. **Use GitOps** for deployment automation (ArgoCD/Flux)

---

For questions or issues, please check the [troubleshooting section](#-troubleshooting) or open an issue on GitHub.
