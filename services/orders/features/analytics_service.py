"""
Unified Analytics Service - รวมทุก features ใน file เดียว
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import time
from collections import defaultdict, deque
from datetime import datetime
from threading import Lock
import json

class AnalyticsService:
    """Unified service ที่รวมทุก feature"""
    
    def __init__(self):
        # Metrics tracking
        self.metrics = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'errors': 0,
            'last_access': None,
            'response_times': deque(maxlen=100)
        })
        self.lock = Lock()
        self.start_time = datetime.now()
    
    # === DATA PROCESSING ===
    def process_data(self, data):
        """ประมวลผลข้อมูลพื้นฐาน"""
        try:
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.read_csv(data) if isinstance(data, str) else data
            
            # Basic cleaning
            df = df.dropna()
            df = df.drop_duplicates()
            
            return {
                'status': 'success',
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'dtypes': df.dtypes.to_dict(),
                'sample': df.head().to_dict('records')
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    # === STATISTICAL ANALYSIS ===
    def analyze_data(self, data):
        """วิเคราะห์เชิงสถิติ"""
        try:
            df = pd.DataFrame(data) if isinstance(data, (dict, list)) else data
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            stats = {}
            for col in numeric_cols:
                stats[col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max())
                }
            
            return {
                'status': 'success',
                'descriptive_stats': stats,
                'correlation': df[numeric_cols].corr().to_dict() if len(numeric_cols) > 1 else {}
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    # === MACHINE LEARNING ===
    def train_model(self, data, target_column):
        """ฝึก ML model แบบง่าย"""
        try:
            df = pd.DataFrame(data) if isinstance(data, (dict, list)) else data
            
            # Prepare features and target
            X = df.select_dtypes(include=[np.number]).drop(columns=[target_column], errors='ignore')
            y = df[target_column]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            model = RandomForestClassifier(n_estimators=10, random_state=42)  # Reduced for speed
            model.fit(X_train, y_train)
            
            # Evaluate
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            
            return {
                'status': 'success',
                'accuracy': float(accuracy),
                'feature_importance': dict(zip(X.columns, model.feature_importances_)),
                'model_type': 'RandomForest'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    # === VISUALIZATION ===
    def create_chart(self, data, chart_type='bar', x_col=None, y_col=None):
        """สร้างกราห์แบบ JSON response (ไม่ใช้ visualization libraries)"""
        try:
            df = pd.DataFrame(data) if isinstance(data, (dict, list)) else data
            
            if chart_type == 'bar' and x_col and y_col:
                chart_data = df.groupby(x_col)[y_col].sum().to_dict()
                return {
                    'status': 'success',
                    'chart_type': 'bar',
                    'data': chart_data,
                    'x_label': x_col,
                    'y_label': y_col
                }
            elif chart_type == 'histogram' and x_col:
                hist_data = df[x_col].value_counts().to_dict()
                return {
                    'status': 'success', 
                    'chart_type': 'histogram',
                    'data': hist_data,
                    'x_label': x_col
                }
            else:
                # Default: correlation matrix for numeric data
                numeric_df = df.select_dtypes(include=[np.number])
                if len(numeric_df.columns) > 1:
                    corr_matrix = numeric_df.corr().round(3).to_dict()
                    return {
                        'status': 'success',
                        'chart_type': 'correlation_matrix',
                        'data': corr_matrix
                    }
                else:
                    return {'status': 'error', 'message': 'Need numeric data for default chart'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    # === DATA VALIDATION ===
    def validate_data(self, data):
        """ตรวจสอบคุณภาพข้อมูล"""
        try:
            df = pd.DataFrame(data) if isinstance(data, (dict, list)) else data
            
            total_cells = df.size
            missing_cells = df.isnull().sum().sum()
            missing_percentage = (missing_cells / total_cells) * 100
            
            duplicates = df.duplicated().sum()
            duplicate_percentage = (duplicates / len(df)) * 100
            
            quality_score = 100 - missing_percentage - duplicate_percentage
            
            return {
                'status': 'success',
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'missing_values': int(missing_cells),
                'missing_percentage': float(missing_percentage),
                'duplicates': int(duplicates),
                'duplicate_percentage': float(duplicate_percentage),
                'quality_score': max(0, float(quality_score))
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    # === METRICS TRACKING ===
    def track_request(self, endpoint, method, status_code, response_time):
        """Track API metrics"""
        with self.lock:
            key = f"{method}:{endpoint}"
            metric = self.metrics[key]
            
            metric['count'] += 1
            metric['total_time'] += response_time
            metric['last_access'] = datetime.now()
            metric['response_times'].append(response_time)
            
            if status_code >= 400:
                metric['errors'] += 1
    
    def get_metrics(self):
        """Get performance metrics"""
        with self.lock:
            result = {}
            for key, metric in self.metrics.items():
                avg_response_time = (
                    metric['total_time'] / metric['count'] 
                    if metric['count'] > 0 else 0
                )
                
                result[key] = {
                    'total_requests': metric['count'],
                    'total_errors': metric['errors'],
                    'error_rate': metric['errors'] / metric['count'] if metric['count'] > 0 else 0,
                    'avg_response_time_ms': round(avg_response_time * 1000, 2),
                    'last_access': metric['last_access'].isoformat() if metric['last_access'] else None
                }
            
            return result
    
    def get_health_status(self):
        """Get service health"""
        with self.lock:
            total_requests = sum(m['count'] for m in self.metrics.values())
            total_errors = sum(m['errors'] for m in self.metrics.values())
            uptime = datetime.now() - self.start_time
            
            return {
                'status': 'healthy',
                'uptime_seconds': int(uptime.total_seconds()),
                'total_requests': total_requests,
                'total_errors': total_errors,
                'error_rate': total_errors / total_requests if total_requests > 0 else 0
            }
