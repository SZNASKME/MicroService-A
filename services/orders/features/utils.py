"""
Common utilities and helper functions
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from functools import wraps
from flask import jsonify

logger = logging.getLogger(__name__)

def handle_api_errors(f):
    """Decorator to handle common API errors"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
    return wrapper

def create_api_response(success: bool = True, data: Any = None, 
                       message: str = None, error: str = None, 
                       status_code: int = 200) -> tuple:
    """Create standardized API response"""
    response = {
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    if error:
        response['error'] = error
    
    return jsonify(response), status_code

def validate_request_data(data: Dict[str, Any], required_fields: list) -> Optional[str]:
    """Validate request data for required fields"""
    if not data:
        return "Request data is required"
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}"
    
    return None