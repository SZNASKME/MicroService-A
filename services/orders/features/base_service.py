"""
Base service class for feature modules
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BaseService(ABC):
    """Base class for all feature services"""
    
    def __init__(self, service_name: str = None):
        self.service_name = service_name or self.__class__.__name__
        self.logger = logging.getLogger(f"{__name__}.{self.service_name}")
        
    def log_error(self, operation: str, error: Exception):
        """Standard error logging"""
        self.logger.error(f"Error in {operation}: {str(error)}")
        
    def create_response(self, success: bool = True, data: Any = None, 
                       message: str = None, error: str = None) -> Dict[str, Any]:
        """Standard response format"""
        response = {
            'success': success,
            'service': self.service_name
        }
        
        if data is not None:
            response['data'] = data
        if message:
            response['message'] = message
        if error:
            response['error'] = error
            
        return response
        
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get service status - must be implemented by subclasses"""
        pass
