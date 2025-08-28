# Visualization packages - make them optional
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

import pandas as pd
import numpy as np
import base64
from io import BytesIO
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class VisualizationService:
    """
    Visualization service for creating charts, graphs, and dashboards
    """
    
    def __init__(self):
        # Set default configuration
        self.supported_chart_types = [
            'line', 'bar', 'scatter', 'histogram', 'box', 'violin',
            'heatmap', 'pie', 'area', 'bubble', 'sunburst'
        ]
        
        # Check for available visualization libraries
        if MATPLOTLIB_AVAILABLE:
            plt.style.use('default')  # Use default instead of seaborn style
        if MATPLOTLIB_AVAILABLE and 'sns' in globals():
            sns.set_palette("husl")
    
    def generate_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate various types of charts
        
        Args:
            data: Dictionary containing chart parameters
            
        Returns:
            Dict containing chart results
        """
        try:
            chart_type = data.get('chart_type', 'bar')
            chart_config = data.get('config', {})
            
            if chart_type not in self.supported_chart_types:
                raise ValueError(f"Unsupported chart type. Supported types: {self.supported_chart_types}")
            
            # Generate sample data for demonstration
            sample_data = self._generate_sample_data(chart_type, chart_config)
            
            # Create chart based on type
            chart_result = self._create_chart(chart_type, sample_data, chart_config)
            
            return {
                'status': 'success',
                'chart_type': chart_type,
                'chart_data': chart_result,
                'metadata': {
                    'generated_at': pd.Timestamp.now().isoformat(),
                    'data_points': len(sample_data.get('x', [])),
                    'chart_config': chart_config
                },
                'message': f'{chart_type.title()} chart generated successfully'
            }
            
        except Exception as e:
            logger.error(f"Error generating chart: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def create_dashboard(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create interactive dashboard with multiple visualizations
        
        Args:
            data: Dictionary containing dashboard parameters
            
        Returns:
            Dict containing dashboard results
        """
        try:
            dashboard_config = data.get('dashboard_config', {})
            chart_configs = data.get('charts', [])
            
            dashboard_charts = []
            
            # Generate multiple charts for dashboard
            for i, chart_config in enumerate(chart_configs):
                chart_type = chart_config.get('type', 'bar')
                chart_title = chart_config.get('title', f'Chart {i+1}')
                
                # Generate sample data
                sample_data = self._generate_sample_data(chart_type, chart_config)
                
                chart_info = {
                    'chart_id': f'chart_{i+1}',
                    'type': chart_type,
                    'title': chart_title,
                    'data': sample_data,
                    'config': chart_config
                }
                
                dashboard_charts.append(chart_info)
            
            # Dashboard layout configuration
            layout_config = {
                'title': dashboard_config.get('title', 'Analytics Dashboard'),
                'theme': dashboard_config.get('theme', 'light'),
                'layout': dashboard_config.get('layout', 'grid'),
                'refresh_interval': dashboard_config.get('refresh_interval', 300)  # seconds
            }
            
            return {
                'status': 'success',
                'dashboard_id': f"dashboard_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}",
                'charts': dashboard_charts,
                'layout_config': layout_config,
                'total_charts': len(dashboard_charts),
                'message': 'Dashboard created successfully'
            }
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def export_visualization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Export visualization in various formats
        
        Args:
            data: Dictionary containing export parameters
            
        Returns:
            Dict containing export results
        """
        try:
            export_format = data.get('format', 'png')  # png, pdf, svg, html
            chart_id = data.get('chart_id')
            quality = data.get('quality', 'high')
            
            # Simulate export process
            export_result = {
                'export_format': export_format,
                'file_size': f"{np.random.randint(100, 1000)} KB",
                'resolution': '1920x1080' if quality == 'high' else '1280x720',
                'export_time': f"{np.random.uniform(0.5, 3.0):.2f} seconds"
            }
            
            return {
                'status': 'success',
                'chart_id': chart_id,
                'export_result': export_result,
                'download_url': f"/api/v1/visualization/download/{chart_id}.{export_format}",
                'message': f'Visualization exported successfully as {export_format.upper()}'
            }
            
        except Exception as e:
            logger.error(f"Error exporting visualization: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _generate_sample_data(self, chart_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate sample data based on chart type"""
        
        data_points = config.get('data_points', 10)
        
        if chart_type in ['line', 'area']:
            return {
                'x': list(range(data_points)),
                'y': [round(np.random.normal(50, 15), 2) for _ in range(data_points)],
                'labels': [f'Point {i+1}' for i in range(data_points)]
            }
        
        elif chart_type in ['bar', 'column']:
            categories = [f'Category {i+1}' for i in range(data_points)]
            return {
                'x': categories,
                'y': [round(np.random.uniform(10, 100), 2) for _ in range(data_points)],
                'labels': categories
            }
        
        elif chart_type == 'scatter':
            return {
                'x': [round(np.random.normal(50, 15), 2) for _ in range(data_points)],
                'y': [round(np.random.normal(50, 15), 2) for _ in range(data_points)],
                'size': [np.random.randint(5, 25) for _ in range(data_points)]
            }
        
        elif chart_type == 'pie':
            categories = [f'Segment {i+1}' for i in range(min(data_points, 8))]
            values = [np.random.randint(10, 100) for _ in range(len(categories))]
            return {
                'labels': categories,
                'values': values
            }
        
        elif chart_type == 'histogram':
            return {
                'values': [np.random.normal(50, 15) for _ in range(data_points * 10)],
                'bins': config.get('bins', 20)
            }
        
        elif chart_type in ['box', 'violin']:
            groups = [f'Group {i+1}' for i in range(min(data_points, 5))]
            return {
                'groups': groups,
                'values': {
                    group: [np.random.normal(50 + i*10, 15) for _ in range(30)]
                    for i, group in enumerate(groups)
                }
            }
        
        elif chart_type == 'heatmap':
            size = min(data_points, 10)
            return {
                'z': [[np.random.uniform(0, 100) for _ in range(size)] for _ in range(size)],
                'x': [f'Col {i+1}' for i in range(size)],
                'y': [f'Row {i+1}' for i in range(size)]
            }
        
        else:
            # Default data structure
            return {
                'x': list(range(data_points)),
                'y': [round(np.random.uniform(0, 100), 2) for _ in range(data_points)]
            }
    
    def _create_chart(self, chart_type: str, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create chart object based on type and data"""
        
        chart_result = {
            'type': chart_type,
            'data': data,
            'styling': {
                'width': config.get('width', 800),
                'height': config.get('height', 600),
                'title': config.get('title', f'{chart_type.title()} Chart'),
                'color_scheme': config.get('color_scheme', 'default'),
                'show_legend': config.get('show_legend', True),
                'show_grid': config.get('show_grid', True)
            },
            'interactive_features': {
                'zoom': config.get('enable_zoom', True),
                'hover': config.get('enable_hover', True),
                'selection': config.get('enable_selection', False)
            }
        }
        
        return chart_result
    
    def get_color_palettes(self) -> Dict[str, Any]:
        """Get available color palettes"""
        return {
            'status': 'success',
            'palettes': {
                'default': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
                'viridis': ['#440154', '#31688e', '#35b779', '#fde725'],
                'plasma': ['#0d0887', '#6a00a8', '#b12a90', '#e16462', '#fca636'],
                'custom_blue': ['#08519c', '#3182bd', '#6baed6', '#9ecae1', '#c6dbef'],
                'custom_green': ['#00441b', '#238b45', '#66c2a4', '#b2e2e2', '#edf8f8']
            },
            'message': 'Color palettes retrieved successfully'
        }
