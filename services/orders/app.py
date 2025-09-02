from flask import Flask, request, jsonify
import logging
from datetime import datetime
import os
import sys

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

# Configure logging for production
def configure_logging():
    """Configure logging for production environment"""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
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

# Production configuration
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-change-in-production'),
    JSON_SORT_KEYS=False,
    JSONIFY_PRETTYPRINT_REGULAR=False,  # Disable pretty print for smaller responses
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
)

# Enable CORS if available
if CORS_AVAILABLE:
    CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))

# Initialize feature services
def create_services():
    """Initialize feature services with error handling"""
    try:
        return {
            'data_processor': DataProcessor(),
            'statistical_analyzer': StatisticalAnalyzer(),
            'visualization_service': VisualizationService(),
            'ml_predictor': MLPredictor(),
            'data_validator': DataValidator(),
            'report_generator': ReportGenerator(),
            'metrics_service': MetricsService()
        }
    except Exception as e:
        logger.error(f"Error initializing services: {str(e)}")
        raise

services = create_services()
data_processor = services['data_processor']
statistical_analyzer = services['statistical_analyzer']
visualization_service = services['visualization_service']
ml_predictor = services['ml_predictor']
data_validator = services['data_validator']
report_generator = services['report_generator']
metrics_service = services['metrics_service']

@app.route('/health', methods=['GET'])
@track_metrics(metrics_service)
def health_check():
    """Health check endpoint for Kubernetes"""
    try:
        # Basic health checks
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'Data Analytics Microservice',
            'version': os.getenv('APP_VERSION', '1.0.0'),
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
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

# Data Processing Endpoints
@app.route('/api/v1/data/upload', methods=['POST'])
@track_metrics(metrics_service)
def upload_data():
    """Upload and process data file"""
    try:
        result = data_processor.upload_and_process(request)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in upload_data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/data/clean', methods=['POST'])
@track_metrics(metrics_service)
def clean_data():
    """Clean and preprocess data"""
    try:
        data = request.get_json()
        result = data_processor.clean_data(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in clean_data: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Statistical Analysis Endpoints
@app.route('/api/v1/analysis/descriptive', methods=['POST'])
@track_metrics(metrics_service)
def descriptive_analysis():
    """Perform descriptive statistical analysis"""
    try:
        data = request.get_json()
        result = statistical_analyzer.descriptive_analysis(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in descriptive_analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/analysis/correlation', methods=['POST'])
def correlation_analysis():
    """Perform correlation analysis"""
    try:
        data = request.get_json()
        result = statistical_analyzer.correlation_analysis(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in correlation_analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Visualization Endpoints
@app.route('/api/v1/visualization/chart', methods=['POST'])
def generate_chart():
    """Generate various types of charts"""
    try:
        data = request.get_json()
        result = visualization_service.generate_chart(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in generate_chart: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/visualization/dashboard', methods=['POST'])
def create_dashboard():
    """Create interactive dashboard"""
    try:
        data = request.get_json()
        result = visualization_service.create_dashboard(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in create_dashboard: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Machine Learning Endpoints
@app.route('/api/v1/ml/train', methods=['POST'])
def train_model():
    """Train machine learning model"""
    try:
        data = request.get_json()
        result = ml_predictor.train_model(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in train_model: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/ml/predict', methods=['POST'])
def make_prediction():
    """Make predictions using trained model"""
    try:
        data = request.get_json()
        result = ml_predictor.predict(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in make_prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Data Validation Endpoints
@app.route('/api/v1/validation/quality', methods=['POST'])
def validate_data_quality():
    """Validate data quality"""
    try:
        data = request.get_json()
        result = data_validator.check_data_quality(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in validate_data_quality: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/validation/schema', methods=['POST'])
def validate_schema():
    """Validate data schema"""
    try:
        data = request.get_json()
        result = data_validator.validate_schema(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in validate_schema: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Report Generation Endpoints
@app.route('/api/v1/reports/generate', methods=['POST'])
def generate_report():
    """Generate comprehensive data analysis report"""
    try:
        data = request.get_json()
        result = report_generator.generate_comprehensive_report(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in generate_report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/reports/export', methods=['POST'])
def export_report():
    """Export report in various formats"""
    try:
        data = request.get_json()
        result = report_generator.export_report(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in export_report: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Metrics & Monitoring Endpoints
@app.route('/api/v1/metrics', methods=['GET'])
@track_metrics(metrics_service)
def get_metrics():
    """Get API metrics in JSON format"""
    try:
        endpoint = request.args.get('endpoint')
        result = metrics_service.get_endpoint_metrics(endpoint)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in get_metrics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/metrics/health', methods=['GET'])
@track_metrics(metrics_service)
def get_health_metrics():
    """Get service health metrics"""
    try:
        result = metrics_service.get_health_metrics()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in get_health_metrics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/metrics', methods=['GET'])
def prometheus_metrics():
    """Get metrics in Prometheus format for monitoring"""
    try:
        result = metrics_service.get_prometheus_metrics()
        return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        logger.error(f"Error in prometheus_metrics: {str(e)}")
        return "# Error generating metrics\n", 500, {'Content-Type': 'text/plain; charset=utf-8'}

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested resource was not found on this server',
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred',
        'status_code': 500
    }), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad request',
        'message': 'The request could not be understood by the server',
        'status_code': 400
    }), 400

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'error': 'Request entity too large',
        'message': 'The uploaded file is too large',
        'status_code': 413
    }), 413

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
