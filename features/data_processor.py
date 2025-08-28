import pandas as pd
import numpy as np
from io import StringIO
import logging
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Data processing service for handling file uploads, cleaning, and preprocessing
    """
    
    def __init__(self):
        self.supported_formats = ['csv', 'json', 'excel', 'parquet']
        self.max_file_size = 50 * 1024 * 1024  # 50MB
    
    def upload_and_process(self, request) -> Dict[str, Any]:
        """
        Upload and process data files
        
        Args:
            request: Flask request object containing file
            
        Returns:
            Dict containing processed data information
        """
        try:
            if 'file' not in request.files:
                raise ValueError("No file provided")
            
            file = request.files['file']
            if file.filename == '':
                raise ValueError("No file selected")
            
            # Check file size
            file.seek(0, 2)  # Seek to end
            file_size = file.tell()
            file.seek(0)  # Reset to beginning
            
            if file_size > self.max_file_size:
                raise ValueError(f"File too large. Maximum size: {self.max_file_size / (1024*1024)}MB")
            
            # Determine file type and process
            filename = file.filename.lower()
            
            if filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif filename.endswith('.json'):
                data = json.load(file)
                df = pd.DataFrame(data) if isinstance(data, list) else pd.json_normalize(data)
            elif filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                raise ValueError(f"Unsupported file format. Supported: {self.supported_formats}")
            
            # Basic data info
            data_info = self._get_data_info(df)
            
            # Store processed data (in production, use proper storage)
            data_id = f"data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            
            return {
                'status': 'success',
                'data_id': data_id,
                'filename': file.filename,
                'file_size': file_size,
                'data_info': data_info,
                'message': 'Data uploaded and processed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error processing upload: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and preprocess data
        
        Args:
            data: Dictionary containing data and cleaning parameters
            
        Returns:
            Dict containing cleaned data results
        """
        try:
            # Extract parameters
            cleaning_options = data.get('cleaning_options', {})
            remove_duplicates = cleaning_options.get('remove_duplicates', True)
            handle_missing = cleaning_options.get('handle_missing', 'drop')
            remove_outliers = cleaning_options.get('remove_outliers', False)
            
            # In a real implementation, you would load the actual data
            # For demo purposes, we'll create sample results
            
            cleaning_results = {
                'original_rows': 1000,
                'cleaned_rows': 950,
                'duplicates_removed': 25,
                'missing_values_handled': 30,
                'outliers_removed': 20 if remove_outliers else 0,
                'cleaning_summary': {
                    'remove_duplicates': remove_duplicates,
                    'missing_value_strategy': handle_missing,
                    'outlier_removal': remove_outliers
                }
            }
            
            return {
                'status': 'success',
                'cleaning_results': cleaning_results,
                'message': 'Data cleaned successfully'
            }
            
        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _get_data_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get basic information about the DataFrame
        
        Args:
            df: pandas DataFrame
            
        Returns:
            Dict containing data information
        """
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'data_types': df.dtypes.astype(str).to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }
    
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply various data transformations
        
        Args:
            data: Dictionary containing transformation parameters
            
        Returns:
            Dict containing transformation results
        """
        try:
            transformations = data.get('transformations', [])
            
            # Sample transformation results
            transformation_results = {
                'applied_transformations': transformations,
                'transformation_count': len(transformations),
                'status': 'completed'
            }
            
            return {
                'status': 'success',
                'transformation_results': transformation_results,
                'message': 'Data transformed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error transforming data: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
