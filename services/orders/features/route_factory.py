"""
Route factory to reduce code duplication in API endpoints
"""
from flask import request
from .utils import handle_api_errors, create_api_response, validate_request_data
from .metrics_service import track_metrics

def create_api_route(service, method_name, required_fields=None, metrics_service=None):
    """Factory function to create standardized API routes"""
    
    @handle_api_errors
    def route_handler():
        # Get request data
        if request.method == 'GET':
            data = request.args.to_dict()
        else:
            data = request.get_json() or {}
        
        # Validate required fields
        if required_fields:
            validation_error = validate_request_data(data, required_fields)
            if validation_error:
                return create_api_response(
                    success=False, 
                    error=validation_error, 
                    status_code=400
                )
        
        # Call service method
        method = getattr(service, method_name)
        result = method(data) if data else method()
        
        return create_api_response(data=result)
    
    # Apply metrics tracking if provided
    if metrics_service:
        route_handler = track_metrics(metrics_service)(route_handler)
    
    return route_handler
