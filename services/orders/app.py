from flask import Flask, request, jsonify
import logging
from datetime import datetime
import os

# Import feature modules
from features.data_processor import DataProcessor
from features.statistical_analyzer import StatisticalAnalyzer
from features.visualization_service import VisualizationService
from features.ml_predictor import MLPredictor
from features.data_validator import DataValidator
from features.report_generator import ReportGenerator

# Try to import CORS, but make it optional
try:
    from flask_cors import CORS
    CORS_AVAILABLE = True
except ImportError:
    CORS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS if available
if CORS_AVAILABLE:
    CORS(app)

# Initialize feature services
data_processor = DataProcessor()
statistical_analyzer = StatisticalAnalyzer()
visualization_service = VisualizationService()
ml_predictor = MLPredictor()
data_validator = DataValidator()
report_generator = ReportGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Data Analytics Microservice'
    })

# Data Processing Endpoints
@app.route('/api/v1/data/upload', methods=['POST'])
def upload_data():
    """Upload and process data file"""
    try:
        result = data_processor.upload_and_process(request)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in upload_data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/data/clean', methods=['POST'])
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create features directory if it doesn't exist
    os.makedirs('features', exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
