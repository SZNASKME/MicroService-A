from flask import Flask, request, jsonify
import logging
from datetime import datetime
import os
import sys
from config import get_config
from features.analytics_service import AnalyticsService

# Initialize analytics service
analytics = AnalyticsService()

# Get configuration
config = get_config()

# Configure logging for production
def configure_logging():
    """Configure production logging"""
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )

def create_app():
    """Application Factory Pattern"""
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Configure logging
    configure_logging()
    logger = logging.getLogger(__name__)
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Global error handler"""
        logger.exception("Unhandled exception occurred")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
    
    # Health Check Endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify(analytics.get_health_status())
    
    # Metrics Endpoint
    @app.route('/metrics')
    def get_metrics():
        """Performance metrics endpoint"""
        return jsonify(analytics.get_metrics())
    
    # === DATA PROCESSING ENDPOINTS ===
    
    @app.route('/api/data/process', methods=['POST'])
    def process_data():
        """Process uploaded data"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'status': 'error', 'message': 'No data provided'}), 400
                
            result = analytics.process_data(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/data/validate', methods=['POST'])
    def validate_data():
        """Validate data quality"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'status': 'error', 'message': 'No data provided'}), 400
                
            result = analytics.validate_data(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    # === ANALYSIS ENDPOINTS ===
    
    @app.route('/api/analysis/stats', methods=['POST'])
    def statistical_analysis():
        """Perform statistical analysis"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'status': 'error', 'message': 'No data provided'}), 400
                
            result = analytics.analyze_data(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    # === MACHINE LEARNING ENDPOINTS ===
    
    @app.route('/api/ml/train', methods=['POST'])
    def train_model():
        """Train ML model"""
        try:
            data = request.get_json()
            if not data or 'target' not in data:
                return jsonify({'status': 'error', 'message': 'Data and target column required'}), 400
                
            target_column = data.pop('target')
            result = analytics.train_model(data, target_column)
            return jsonify(result)
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    # === VISUALIZATION ENDPOINTS ===
    
    @app.route('/api/viz/chart', methods=['POST'])
    def create_chart():
        """Create visualization chart"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'status': 'error', 'message': 'No data provided'}), 400
                
            chart_type = data.pop('chart_type', 'bar')
            x_col = data.pop('x_column', None)
            y_col = data.pop('y_column', None)
            
            result = analytics.create_chart(data, chart_type, x_col, y_col)
            return jsonify(result)
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
