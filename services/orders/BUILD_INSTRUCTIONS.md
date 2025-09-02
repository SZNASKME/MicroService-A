# 🐳 Docker Build Instructions - Updated

## ✅ Prerequisites Fixed

1. **Correct build context**: Use `services/orders/` as build context
2. **Dockerfile casing**: Fixed `as` to `AS`
3. **Clean dependencies**: Removed dev dependencies
4. **Optimized .dockerignore**: Exclude unnecessary files

## 🚀 Quick Build Commands

### For Production (Multi-platform)
```bash
# From repository root
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -f services/orders/Dockerfile \
  -t ghcr.io/sznaskme/microservice-a/orders:latest \
  --push \
  services/orders/
```

### For Local Testing
```bash
# From repository root
docker build \
  -f services/orders/Dockerfile \
  -t microservice-a-orders:local \
  services/orders/

# Run locally
docker run -p 5000:5000 microservice-a-orders:local
```

## 🛠️ Build Scripts

### Production Build
```bash
# Make executable and run
chmod +x services/orders/build-prod.sh
./services/orders/build-prod.sh

# With specific version
./services/orders/build-prod.sh v1.0.1
```

### Local Build
```bash
# Make executable and run
chmod +x services/orders/build-local.sh
./services/orders/build-local.sh
```

## 📁 Correct Directory Structure

The build expects this structure:
```
MicroService-A/                 ← Repository root (run commands from here)
├── services/
│   └── orders/                 ← Build context
│       ├── Dockerfile          ← -f services/orders/Dockerfile
│       ├── requirements.txt    ← Dependencies
│       ├── app.py              ← Main application
│       ├── wsgi.py             ← WSGI entry point
│       ├── config.py           ← Configuration
│       ├── .env.production     ← Production env vars
│       ├── .dockerignore       ← Ignore rules
│       └── features/           ← Feature modules
│           ├── __init__.py
│           └── *.py
```

## 🔧 What Was Fixed

1. **Dockerfile Improvements**:
   - ✅ Fixed casing: `FROM python:3.9-slim AS builder`
   - ✅ Added `--no-install-recommends` for smaller image
   - ✅ Explicit file copying instead of `COPY . .`
   - ✅ Better layer optimization

2. **Dependencies Cleaned**:
   - ✅ Removed pytest, black, flake8 from requirements.txt
   - ✅ Only production dependencies remain
   - ✅ Smaller final image size

3. **Build Context Optimized**:
   - ✅ Enhanced .dockerignore
   - ✅ Excludes test files, docs, dev configs
   - ✅ Faster builds, smaller context

4. **Security Improvements**:
   - ✅ Explicit file copying
   - ✅ Proper file ownership
   - ✅ Non-root user
   - ✅ No sensitive files in image

## 🎯 Expected Results

- **Image Size**: ~300MB (down from ~400MB+)
- **Build Time**: 2-3 minutes (with cache)
- **Platforms**: linux/amd64, linux/arm64
- **Security**: Non-root user, minimal surface
- **Performance**: Optimized gunicorn settings

## 🚨 Common Issues Fixed

1. **"requirements.txt not found"** → Use correct build context
2. **"FromAsCasing warning"** → Fixed casing in Dockerfile
3. **Large image size** → Removed dev dependencies
4. **Slow builds** → Optimized .dockerignore
5. **Security warnings** → Non-root user, explicit copying
