import time
import functools
from collections import defaultdict, deque
from datetime import datetime, timedelta
from threading import Lock
import json

class MetricsService:
    def __init__(self):
        self.metrics = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'errors': 0,
            'last_access': None,
            'response_times': deque(maxlen=100)  # Keep last 100 response times
        })
        self.lock = Lock()
        self.start_time = datetime.now()
        
    def track_request(self, endpoint, method, status_code, response_time):
        """Track API request metrics"""
        with self.lock:
            key = f"{method}:{endpoint}"
            metric = self.metrics[key]
            
            metric['count'] += 1
            metric['total_time'] += response_time
            metric['last_access'] = datetime.now()
            metric['response_times'].append(response_time)
            
            if status_code >= 400:
                metric['errors'] += 1
    
    def get_endpoint_metrics(self, endpoint=None):
        """Get metrics for specific endpoint or all endpoints"""
        with self.lock:
            if endpoint:
                return dict(self.metrics.get(endpoint, {}))
            
            result = {}
            for key, metric in self.metrics.items():
                avg_response_time = (
                    metric['total_time'] / metric['count'] 
                    if metric['count'] > 0 else 0
                )
                
                recent_times = list(metric['response_times'])
                p95_response_time = (
                    sorted(recent_times)[int(len(recent_times) * 0.95)] 
                    if recent_times else 0
                )
                
                result[key] = {
                    'total_requests': metric['count'],
                    'total_errors': metric['errors'],
                    'error_rate': metric['errors'] / metric['count'] if metric['count'] > 0 else 0,
                    'avg_response_time_ms': round(avg_response_time * 1000, 2),
                    'p95_response_time_ms': round(p95_response_time * 1000, 2),
                    'last_access': metric['last_access'].isoformat() if metric['last_access'] else None
                }
            
            return result
    
    def get_health_metrics(self):
        """Get overall service health metrics"""
        with self.lock:
            total_requests = sum(m['count'] for m in self.metrics.values())
            total_errors = sum(m['errors'] for m in self.metrics.values())
            
            uptime = datetime.now() - self.start_time
            
            return {
                'uptime_seconds': int(uptime.total_seconds()),
                'uptime_human': str(uptime),
                'total_requests': total_requests,
                'total_errors': total_errors,
                'overall_error_rate': total_errors / total_requests if total_requests > 0 else 0,
                'endpoints_count': len(self.metrics),
                'service_status': 'healthy' if total_errors / total_requests < 0.05 else 'degraded' if total_requests > 0 else 'unknown'
            }
    
    def get_prometheus_metrics(self):
        """Get metrics in Prometheus format for monitoring"""
        lines = []
        
        # Service uptime
        uptime = (datetime.now() - self.start_time).total_seconds()
        lines.append(f"# HELP service_uptime_seconds Service uptime in seconds")
        lines.append(f"# TYPE service_uptime_seconds counter")
        lines.append(f"service_uptime_seconds {uptime}")
        
        with self.lock:
            for endpoint, metric in self.metrics.items():
                method, path = endpoint.split(':', 1)
                labels = f'method="{method}",endpoint="{path}"'
                
                # Request count
                lines.append(f"# HELP http_requests_total Total number of HTTP requests")
                lines.append(f"# TYPE http_requests_total counter")
                lines.append(f"http_requests_total{{{labels}}} {metric['count']}")
                
                # Error count
                lines.append(f"# HELP http_errors_total Total number of HTTP errors")
                lines.append(f"# TYPE http_errors_total counter")
                lines.append(f"http_errors_total{{{labels}}} {metric['errors']}")
                
                # Average response time
                avg_time = metric['total_time'] / metric['count'] if metric['count'] > 0 else 0
                lines.append(f"# HELP http_request_duration_seconds Average request duration")
                lines.append(f"# TYPE http_request_duration_seconds gauge")
                lines.append(f"http_request_duration_seconds{{{labels}}} {avg_time}")
        
        return '\n'.join(lines)

def track_metrics(metrics_service):
    """Decorator to track API endpoint metrics"""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                # Get request info
                from flask import request
                endpoint = request.endpoint or 'unknown'
                method = request.method
                
                # Execute the function
                result = f(*args, **kwargs)
                
                # Calculate response time
                response_time = time.time() - start_time
                
                # Determine status code
                if hasattr(result, 'status_code'):
                    status_code = result.status_code
                elif isinstance(result, tuple) and len(result) >= 2:
                    status_code = result[1]
                else:
                    status_code = 200
                
                # Track metrics
                metrics_service.track_request(endpoint, method, status_code, response_time)
                
                return result
                
            except Exception as e:
                # Track error
                response_time = time.time() - start_time
                from flask import request
                endpoint = request.endpoint or 'unknown'
                method = request.method
                metrics_service.track_request(endpoint, method, 500, response_time)
                raise
        
        return wrapper
    return decorator
