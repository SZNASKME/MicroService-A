# 🚀 Production Deployment Guide

## Prerequisites

1. **Environment Setup**
   ```bash
   # Copy production environment file
   cp .env.production .env
   
   # Edit environment variables
   nano .env
   ```

2. **Required Environment Variables**
   - `SECRET_KEY`: Strong secret key for Flask
   - `FLASK_ENV=production`
   - `LOG_LEVEL=WARNING`
   - `CORS_ORIGINS`: Allowed origins (comma-separated)

## Local Production Testing

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Production Server
```bash
# Linux/Mac
./start.sh

# Windows
start.bat

# Manual
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:application
```

### 3. Test Production Readiness
```bash
python test_production.py
```

## Docker Deployment

### 1. Build Image
```bash
docker build -t microservice-a-orders:v1.0.0 .
```

### 2. Run Container
```bash
docker run -d \
  --name microservice-a-orders \
  -p 5000:5000 \
  --env-file .env.production \
  microservice-a-orders:v1.0.0
```

### 3. Health Check
```bash
curl http://localhost:5000/health
```

## Kubernetes Deployment

### 1. Create ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: microservice-a-config
data:
  FLASK_ENV: "production"
  LOG_LEVEL: "WARNING"
  CORS_ORIGINS: "https://yourdomain.com"
```

### 2. Create Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: microservice-a-secret
type: Opaque
data:
  SECRET_KEY: <base64-encoded-secret>
```

### 3. Deploy Application
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: microservice-a-orders
spec:
  replicas: 3
  selector:
    matchLabels:
      app: microservice-a-orders
  template:
    metadata:
      labels:
        app: microservice-a-orders
    spec:
      containers:
      - name: app
        image: microservice-a-orders:v1.0.0
        ports:
        - containerPort: 5000
        envFrom:
        - configMapRef:
            name: microservice-a-config
        - secretRef:
            name: microservice-a-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 4. Create Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: microservice-a-service
spec:
  selector:
    app: microservice-a-orders
  ports:
  - port: 80
    targetPort: 5000
  type: ClusterIP
```

## Monitoring Setup

### 1. Prometheus ServiceMonitor
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: microservice-a-metrics
spec:
  selector:
    matchLabels:
      app: microservice-a-orders
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### 2. Grafana Dashboard
- Import dashboard using metrics from `/metrics` endpoint
- Key metrics to monitor:
  - `http_requests_total`
  - `http_request_duration_seconds`
  - `service_uptime_seconds`

## Security Checklist

- [ ] Secret key is strong and unique
- [ ] CORS origins are properly configured
- [ ] Running as non-root user
- [ ] File permissions are restrictive
- [ ] Logs don't contain sensitive data
- [ ] Error messages don't expose internal details

## Performance Optimization

### 1. Gunicorn Configuration
```bash
# Optimal settings for production
gunicorn \
  --bind 0.0.0.0:5000 \
  --workers $((2 * $(nproc) + 1)) \
  --worker-class sync \
  --worker-connections 1000 \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  --timeout 30 \
  --keep-alive 2 \
  --preload \
  wsgi:application
```

### 2. Resource Limits
- **Memory**: 256Mi request, 512Mi limit
- **CPU**: 250m request, 500m limit
- **Disk**: Persistent storage for logs/uploads

## Troubleshooting

### Common Issues

1. **Health check failing**
   ```bash
   # Check logs
   kubectl logs deployment/microservice-a-orders
   
   # Check service
   kubectl get svc microservice-a-service
   ```

2. **High memory usage**
   - Check for memory leaks in data processing
   - Reduce worker count if needed
   - Monitor metrics endpoint

3. **Slow response times**
   - Check database connections
   - Monitor CPU/memory usage
   - Scale horizontally if needed

### Logs Analysis
```bash
# Application logs
tail -f logs/app.log

# Access logs
tail -f logs/access.log

# Error logs
tail -f logs/error.log
```

## Backup and Recovery

### Data Backup
- Upload files: `/app/uploads`
- Logs: `/app/logs`
- Configuration: Environment variables

### Recovery Procedure
1. Restore configuration
2. Rebuild and deploy container
3. Restore upload files
4. Verify health checks

## Scaling Guidelines

### Horizontal Scaling
- Start with 3 replicas
- Scale based on CPU/memory usage
- Monitor request latency

### Vertical Scaling
- Increase memory for large data processing
- Add CPU for intensive computations
- Monitor resource usage patterns
