# Configuration file for Data Analytics Microservice
import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Application Configuration
    APP_NAME = 'Data Analytics Microservice'
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Data Processing Configuration
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 50 * 1024 * 1024))  # 50MB
    SUPPORTED_FILE_FORMATS = ['csv', 'json', 'xlsx', 'xls', 'parquet']
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')

    # Machine Learning Configuration
    DEFAULT_TEST_SIZE = float(os.getenv('DEFAULT_TEST_SIZE', 0.2))
    DEFAULT_RANDOM_STATE = int(os.getenv('DEFAULT_RANDOM_STATE', 42))
    DEFAULT_CV_FOLDS = int(os.getenv('DEFAULT_CV_FOLDS', 5))

    # Visualization Configuration
    DEFAULT_CHART_WIDTH = int(os.getenv('DEFAULT_CHART_WIDTH', 800))
    DEFAULT_CHART_HEIGHT = int(os.getenv('DEFAULT_CHART_HEIGHT', 600))
    SUPPORTED_CHART_TYPES = [
        'line', 'bar', 'scatter', 'histogram', 'box', 'violin',
        'heatmap', 'pie', 'area', 'bubble', 'sunburst'
    ]

    # Data Validation Configuration
    DEFAULT_QUALITY_THRESHOLD = float(os.getenv('DEFAULT_QUALITY_THRESHOLD', 0.8))
    DEFAULT_MISSING_THRESHOLD = float(os.getenv('DEFAULT_MISSING_THRESHOLD', 0.05))
    DEFAULT_OUTLIER_THRESHOLD = float(os.getenv('DEFAULT_OUTLIER_THRESHOLD', 0.03))

    # Report Configuration
    REPORT_EXPORT_FORMATS = ['pdf', 'html', 'docx', 'json', 'csv']
    DEFAULT_REPORT_TEMPLATE = os.getenv('DEFAULT_REPORT_TEMPLATE', 'detailed_analysis')
    REPORT_RETENTION_DAYS = int(os.getenv('REPORT_RETENTION_DAYS', 30))

    # External Services
    EXTERNAL_API_TIMEOUT = int(os.getenv('EXTERNAL_API_TIMEOUT', 30))
    
    # Database Configuration (if needed in future)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Redis Configuration (if needed for caching)
    REDIS_URL = os.getenv('REDIS_URL')
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_') and not callable(getattr(cls, key))
        }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    JSONIFY_PRETTYPRINT_REGULAR = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING')
    
    # Security headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}

def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'production')
    
    return config_map.get(env, config_map['default'])
SECRET_KEY = 'your-secret-key-here'
JWT_SECRET_KEY = 'your-jwt-secret-key'
JWT_EXPIRATION_HOURS = 24

# Database Configuration (for future implementation)
DATABASE_URL = 'sqlite:///data_analytics.db'
REDIS_URL = 'redis://localhost:6379/0'

# External API Configuration (if needed)
EXTERNAL_API_TIMEOUT = 30
EXTERNAL_API_RETRIES = 3

# Caching Configuration
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes

# Feature Flags
ENABLE_ML_FEATURES = True
ENABLE_ADVANCED_ANALYTICS = True
ENABLE_REAL_TIME_PROCESSING = False
ENABLE_DATA_STREAMING = False
