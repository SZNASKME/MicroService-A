from flask import Flask, request, jsonify
import logging
from datetime import datetime
import os
import sys
from config import get_config
from features.utils import handle_api_errors, create_api_response
from features.route_factory import create_api_route

# Import feature modules
from features.data_processor import DataProcessor
from features.statistical_analyzer import StatisticalAnalyzer
from features.visualization_service import VisualizationService
from features.ml_predictor import MLPredictor
from features.data_validator import DataValidator
from features.report_generator import ReportGenerator
from features.metrics_service import MetricsService, track_metrics

# Try to import CORS, but make it optional
try:
    from flask_cors import CORS
    CORS_AVAILABLE = True
except ImportError:
    CORS_AVAILABLE = False

# Get configuration
config = get_config()

# Configure logging for production
def configure_logging():
    """Configure logging for production environment"""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format=config.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/app.log') if os.path.exists('logs') else logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Suppress noisy logs in production
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

logger = configure_logging()

app = Flask(__name__)

# Apply configuration
app.config.from_object(config)

# Enable CORS if available
if CORS_AVAILABLE:
    CORS(app, origins=config.CORS_ORIGINS)

# Initialize feature services
def create_services():
    """Initialize feature services with error handling"""
    services = [
        DataProcessor(), StatisticalAnalyzer(), VisualizationService(),
        MLPredictor(), DataValidator(), ReportGenerator(), MetricsService()
    ]
    return services

data_processor, statistical_analyzer, visualization_service, ml_predictor, \
data_validator, report_generator, metrics_service = create_services()

@app.route('/health', methods=['GET'])
@track_metrics(metrics_service)
def health_check():
    """Health check endpoint for Kubernetes"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': config.APP_NAME,
        'version': config.APP_VERSION,
        'environment': os.getenv('FLASK_ENV', 'production')
    }
    
    # Optional detailed health check
    if request.args.get('detailed') == 'true':
        health_status['services'] = {
            'data_processor': 'healthy',
            'statistical_analyzer': 'healthy',
            'visualization_service': 'healthy',
            'ml_predictor': 'healthy',
            'data_validator': 'healthy',
            'report_generator': 'healthy'
        }
    
    return jsonify(health_status)

# Data Processing Endpoints
app.add_url_rule('/api/v1/data/upload', 'upload_data', 
                 create_api_route(data_processor, 'upload_and_process', metrics_service=metrics_service), 
                 methods=['POST'])

app.add_url_rule('/api/v1/data/clean', 'clean_data',
                 create_api_route(data_processor, 'clean_data', metrics_service=metrics_service),
                 methods=['POST'])

# Statistical Analysis Endpoints  
app.add_url_rule('/api/v1/analysis/descriptive', 'descriptive_analysis',
                 create_api_route(statistical_analyzer, 'descriptive_analysis', metrics_service=metrics_service),
                 methods=['POST'])

app.add_url_rule('/api/v1/analysis/correlation', 'correlation_analysis',
                 create_api_route(statistical_analyzer, 'correlation_analysis', metrics_service=metrics_service),
                 methods=['POST'])

# Register all API endpoints using route factory
def register_api_routes():
    """Register all API routes using the route factory"""
    routes = [
        # Visualization Endpoints
        ('/api/v1/visualization/chart', 'generate_chart', visualization_service, 'generate_chart'),
        ('/api/v1/visualization/dashboard', 'create_dashboard', visualization_service, 'create_dashboard'),
        
        # Machine Learning Endpoints  
        ('/api/v1/ml/train', 'train_model', ml_predictor, 'train_model'),
        ('/api/v1/ml/predict', 'make_prediction', ml_predictor, 'predict'),
        
        # Data Validation Endpoints
        ('/api/v1/validation/quality', 'validate_data_quality', data_validator, 'check_data_quality'),
        ('/api/v1/validation/schema', 'validate_schema', data_validator, 'validate_schema'),
        
        # Report Generation Endpoints
        ('/api/v1/reports/generate', 'generate_report', report_generator, 'generate_comprehensive_report'),
        ('/api/v1/reports/export', 'export_report', report_generator, 'export_report'),
        
        # Metrics Endpoints
        ('/api/v1/metrics', 'get_metrics', metrics_service, 'get_endpoint_metrics'),
        ('/api/v1/metrics/health', 'get_health_metrics', metrics_service, 'get_health_metrics'),
    ]
    
    for url, endpoint, service, method in routes:
        app.add_url_rule(url, endpoint,
                        create_api_route(service, method, metrics_service=metrics_service),
                        methods=['POST', 'GET'])

register_api_routes()

@app.route('/metrics', methods=['GET'])
def prometheus_metrics():
    """Get metrics in Prometheus format for monitoring"""
    try:
        result = metrics_service.get_prometheus_metrics()
        return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        logger.error(f"Error in prometheus_metrics: {str(e)}")
        return "# Error generating metrics\n", 500, {'Content-Type': 'text/plain; charset=utf-8'}

# Error handlers
error_handlers = {
    404: ('Endpoint not found', 'The requested resource was not found on this server'),
    400: ('Bad request', 'The request could not be understood by the server'),
    413: ('Request entity too large', 'The uploaded file is too large'),
    500: ('Internal server error', 'An unexpected error occurred')
}

def create_error_handler(status_code):
    """Factory function to create error handlers"""
    def handler(error):
        if status_code == 500:
            logger.error(f"Internal server error: {str(error)}")
        
        error_title, error_message = error_handlers[status_code]
        return create_api_response(
            success=False,
            error=error_title,
            message=error_message,
            status_code=status_code
        )
    return handler

# Register error handlers
for code in error_handlers:
    app.errorhandler(code)(create_error_handler(code))

def create_app():
    """Application factory for production deployment"""
    # Create required directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    
    logger.info("Application starting...")
    logger.info(f"Environment: {os.getenv('FLASK_ENV', 'production')}")
    logger.info(f"Version: {os.getenv('APP_VERSION', '1.0.0')}")
    
    return app

if __name__ == '__main__':
    # Development mode only
    create_app()
    app.run(
        debug=os.getenv('FLASK_ENV') == 'development',
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000))
    )
else:
    # Production mode (when running with gunicorn)
    application = create_app()
