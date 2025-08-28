# Configuration file for Data Analytics Microservice

# Server Configuration
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# Data Processing Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
SUPPORTED_FILE_FORMATS = ['csv', 'json', 'xlsx', 'xls', 'parquet']
UPLOAD_FOLDER = 'uploads'

# Machine Learning Configuration
DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42
DEFAULT_CV_FOLDS = 5

# Visualization Configuration
DEFAULT_CHART_WIDTH = 800
DEFAULT_CHART_HEIGHT = 600
SUPPORTED_CHART_TYPES = [
    'line', 'bar', 'scatter', 'histogram', 'box', 'violin',
    'heatmap', 'pie', 'area', 'bubble', 'sunburst'
]

# Data Validation Configuration
DEFAULT_QUALITY_THRESHOLD = 0.8
DEFAULT_MISSING_THRESHOLD = 0.05
DEFAULT_OUTLIER_THRESHOLD = 0.03

# Report Configuration
REPORT_EXPORT_FORMATS = ['pdf', 'html', 'docx', 'json', 'csv']
DEFAULT_REPORT_TEMPLATE = 'detailed_analysis'
REPORT_RETENTION_DAYS = 30

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Security Configuration (for future implementation)
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
