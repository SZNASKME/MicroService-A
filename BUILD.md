# 🐳 Docker Build Instructions

## Quick Build

### Linux/Mac
```bash
# Build and push to registry
./build.sh

# Build specific version
./build.sh v1.0.1
```

### Windows
```cmd
# Build and push to registry
build.bat

# Build specific version
build.bat v1.0.1
```

## Manual Build Commands

### Single Platform (Local Testing)
```bash
# Build for local testing
docker build -t microservice-a-orders:latest -f services/orders/Dockerfile services/orders/

# Run locally
docker run -p 5000:5000 microservice-a-orders:latest
```

### Multi-Platform (Production)
```bash
# Create builder
docker buildx create --name microservice-builder --use

# Build and push multi-platform
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --cache-from type=registry,ref=ghcr.io/sznaskme/microservice-a/orders:cache \
  --cache-to type=registry,ref=ghcr.io/sznaskme/microservice-a/orders:cache,mode=max \
  -f services/orders/Dockerfile \
  -t ghcr.io/sznaskme/microservice-a/orders:latest \
  --push \
  services/orders/
```

## Build Context Structure

The correct build context is `services/orders/` which contains:
```
services/orders/
├── Dockerfile
├── requirements.txt
├── app.py
├── wsgi.py
├── config.py
├── .dockerignore
├── features/
│   ├── __init__.py
│   ├── *.py (feature modules)
└── other files...
```

## Common Issues

### ❌ Error: requirements.txt not found
**Problem:** Using wrong build context
```bash
# Wrong - missing context path
docker build -f services/orders/Dockerfile .

# Correct - specify context
docker build -f services/orders/Dockerfile services/orders/
```

### ❌ Warning: 'as' and 'FROM' keywords' casing
**Solution:** Use uppercase `AS` in Dockerfile
```dockerfile
# Wrong
FROM python:3.9-slim as builder

# Correct
FROM python:3.9-slim AS builder
```

### ❌ Build fails with file not found
**Check:**
1. You're in the repository root directory
2. Build context path is correct: `services/orders/`
3. All required files exist in the context

## Image Details

- **Base Image:** python:3.9-slim
- **Architecture:** linux/amd64, linux/arm64
- **Size:** ~300MB (optimized with multi-stage build)
- **User:** non-root (appuser)
- **Port:** 5000
- **Health Check:** `/health` endpoint

## Registry

Images are pushed to GitHub Container Registry:
- `ghcr.io/sznaskme/microservice-a/orders:latest`
- `ghcr.io/sznaskme/microservice-a/orders:v1.0.0`
