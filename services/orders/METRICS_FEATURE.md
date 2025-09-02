# 📊 Metrics & Monitoring Feature

เพิ่ม API Metrics และ Monitoring capabilities ให้กับ Data Analytics Microservice

## ✨ Features

### 1. **Request Tracking**
- ติดตาม request count, response time, error rate
- เก็บ 95th percentile response time
- Track ได้ทุก endpoint

### 2. **Health Monitoring** 
- Service uptime
- Overall error rate
- Service status (healthy/degraded)

### 3. **Prometheus Integration**
- Export metrics ในรูปแบบ Prometheus
- พร้อมใช้กับ Grafana dashboard
- Support Kubernetes monitoring

## 🔗 API Endpoints

### JSON Metrics
```
GET /api/v1/metrics
GET /api/v1/metrics?endpoint=health_check
GET /api/v1/metrics/health
```

### Prometheus Metrics
```
GET /metrics
```

## 📈 Metrics Types

### Endpoint Metrics
```json
{
  "GET:health_check": {
    "total_requests": 100,
    "total_errors": 0,
    "error_rate": 0.0,
    "avg_response_time_ms": 15.23,
    "p95_response_time_ms": 25.67,
    "last_access": "2025-09-02T10:30:00"
  }
}
```

### Health Metrics
```json
{
  "uptime_seconds": 3600,
  "uptime_human": "1:00:00",
  "total_requests": 500,
  "total_errors": 2,
  "overall_error_rate": 0.004,
  "endpoints_count": 15,
  "service_status": "healthy"
}
```

## 🚀 Usage Examples

### Get All Endpoint Metrics
```bash
curl http://localhost:5000/api/v1/metrics
```

### Get Specific Endpoint Metrics
```bash
curl http://localhost:5000/api/v1/metrics?endpoint=upload_data
```

### Get Service Health
```bash
curl http://localhost:5000/api/v1/metrics/health
```

### Get Prometheus Metrics
```bash
curl http://localhost:5000/metrics
```

## 🧪 Testing

Run the test script:
```bash
python test_metrics.py
```

## 🔧 Kubernetes Integration

### ServiceMonitor for Prometheus
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: microservice-a-metrics
spec:
  selector:
    matchLabels:
      app: microservice-a
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### Health Check
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /api/v1/metrics/health
    port: 5000
  initialDelaySeconds: 5
  periodSeconds: 5
```

## 📊 Grafana Dashboard

Metrics ที่สามารถใช้ใน Grafana:
- `http_requests_total` - Total requests
- `http_errors_total` - Total errors  
- `http_request_duration_seconds` - Response time
- `service_uptime_seconds` - Service uptime

## 🔐 Security

- ไม่เก็บ sensitive data ใน metrics
- Metrics endpoint ไม่ต้อง authentication (standard practice)
- Thread-safe implementation

## ⚡ Performance

- Low overhead tracking
- Efficient memory usage (fixed-size deques)
- Thread-safe operations
- Minimal impact on response time (<1ms)
