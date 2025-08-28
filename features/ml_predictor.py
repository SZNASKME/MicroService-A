from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pandas as pd
import numpy as np
import pickle
import logging
from typing import Dict, Any, Optional, Tuple
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class MLPredictor:
    """
    Machine Learning service for training models and making predictions
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.model_metadata = {}
        
        # Supported algorithms
        self.classification_algorithms = {
            'random_forest': RandomForestClassifier,
            'logistic_regression': LogisticRegression,
            'svm': SVC
        }
        
        self.regression_algorithms = {
            'random_forest': RandomForestRegressor,
            'linear_regression': LinearRegression,
            'svm': SVR
        }
    
    def train_model(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Train a machine learning model
        
        Args:
            data: Dictionary containing training parameters
            
        Returns:
            Dict containing training results
        """
        try:
            # Extract parameters
            model_type = data.get('model_type', 'classification')  # classification or regression
            algorithm = data.get('algorithm', 'random_forest')
            model_name = data.get('model_name', f'model_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            
            # Training configuration
            test_size = data.get('test_size', 0.2)
            random_state = data.get('random_state', 42)
            cv_folds = data.get('cv_folds', 5)
            
            # In production, you would load actual data
            # For demo, we'll simulate training process
            
            # Generate sample training data
            n_samples = data.get('n_samples', 1000)
            n_features = data.get('n_features', 10)
            
            X, y = self._generate_sample_data(model_type, n_samples, n_features)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            
            # Select and train model
            if model_type == 'classification':
                if algorithm not in self.classification_algorithms:
                    raise ValueError(f"Unsupported classification algorithm: {algorithm}")
                model_class = self.classification_algorithms[algorithm]
            else:
                if algorithm not in self.regression_algorithms:
                    raise ValueError(f"Unsupported regression algorithm: {algorithm}")
                model_class = self.regression_algorithms[algorithm]
            
            # Initialize and train model
            model = model_class(random_state=random_state)
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            if model_type == 'classification':
                accuracy = accuracy_score(y_test, y_pred)
                cv_scores = cross_val_score(model, X_train, y_train, cv=cv_folds)
                
                metrics = {
                    'accuracy': round(accuracy, 4),
                    'cv_mean': round(cv_scores.mean(), 4),
                    'cv_std': round(cv_scores.std(), 4),
                    'test_samples': len(y_test)
                }
            else:
                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)
                cv_scores = cross_val_score(model, X_train, y_train, cv=cv_folds, scoring='neg_mean_squared_error')
                
                metrics = {
                    'mse': round(mse, 4),
                    'rmse': round(rmse, 4),
                    'cv_mean': round(-cv_scores.mean(), 4),
                    'cv_std': round(cv_scores.std(), 4),
                    'test_samples': len(y_test)
                }
            
            # Store model
            self.models[model_name] = model
            self.model_metadata[model_name] = {
                'model_type': model_type,
                'algorithm': algorithm,
                'trained_at': datetime.now().isoformat(),
                'n_features': n_features,
                'training_samples': len(X_train),
                'metrics': metrics
            }
            
            return {
                'status': 'success',
                'model_name': model_name,
                'model_type': model_type,
                'algorithm': algorithm,
                'metrics': metrics,
                'training_info': {
                    'training_samples': len(X_train),
                    'test_samples': len(X_test),
                    'features': n_features,
                    'cv_folds': cv_folds
                },
                'message': f'Model {model_name} trained successfully'
            }
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make predictions using a trained model
        
        Args:
            data: Dictionary containing prediction parameters
            
        Returns:
            Dict containing prediction results
        """
        try:
            model_name = data.get('model_name')
            
            if not model_name:
                raise ValueError("Model name is required")
            
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
            
            model = self.models[model_name]
            metadata = self.model_metadata[model_name]
            
            # Generate sample prediction data
            n_predictions = data.get('n_predictions', 10)
            n_features = metadata['n_features']
            
            # Generate random input data for demonstration
            X_new = np.random.randn(n_predictions, n_features)
            
            # Make predictions
            predictions = model.predict(X_new)
            
            # Get prediction probabilities for classification
            prediction_results = []
            
            for i, pred in enumerate(predictions):
                result = {
                    'prediction_id': i + 1,
                    'predicted_value': float(pred) if metadata['model_type'] == 'regression' else int(pred)
                }
                
                # Add probabilities for classification
                if metadata['model_type'] == 'classification' and hasattr(model, 'predict_proba'):
                    probabilities = model.predict_proba(X_new[i:i+1])[0]
                    result['probabilities'] = {
                        f'class_{j}': round(float(prob), 4) 
                        for j, prob in enumerate(probabilities)
                    }
                    result['confidence'] = round(float(max(probabilities)), 4)
                
                prediction_results.append(result)
            
            return {
                'status': 'success',
                'model_name': model_name,
                'model_info': {
                    'type': metadata['model_type'],
                    'algorithm': metadata['algorithm'],
                    'trained_at': metadata['trained_at']
                },
                'predictions': prediction_results,
                'prediction_count': len(prediction_results),
                'message': f'Predictions generated successfully using {model_name}'
            }
            
        except Exception as e:
            logger.error(f"Error making predictions: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def evaluate_model(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate model performance
        
        Args:
            data: Dictionary containing evaluation parameters
            
        Returns:
            Dict containing evaluation results
        """
        try:
            model_name = data.get('model_name')
            
            if not model_name or model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
            
            metadata = self.model_metadata[model_name]
            
            # Return stored metrics and additional evaluation info
            evaluation_results = {
                'model_performance': metadata['metrics'],
                'model_info': {
                    'type': metadata['model_type'],
                    'algorithm': metadata['algorithm'],
                    'training_samples': metadata['training_samples'],
                    'features': metadata['n_features']
                },
                'feature_importance': self._get_feature_importance(model_name),
                'evaluation_timestamp': datetime.now().isoformat()
            }
            
            return {
                'status': 'success',
                'model_name': model_name,
                'evaluation_results': evaluation_results,
                'message': f'Model {model_name} evaluated successfully'
            }
            
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def list_models(self) -> Dict[str, Any]:
        """
        List all trained models
        
        Returns:
            Dict containing list of models
        """
        try:
            models_list = []
            
            for model_name, metadata in self.model_metadata.items():
                model_info = {
                    'name': model_name,
                    'type': metadata['model_type'],
                    'algorithm': metadata['algorithm'],
                    'trained_at': metadata['trained_at'],
                    'training_samples': metadata['training_samples'],
                    'features': metadata['n_features'],
                    'performance': metadata['metrics']
                }
                models_list.append(model_info)
            
            return {
                'status': 'success',
                'models': models_list,
                'total_models': len(models_list),
                'message': 'Models listed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _generate_sample_data(self, model_type: str, n_samples: int, n_features: int) -> Tuple[np.ndarray, np.ndarray]:
        """Generate sample data for training"""
        
        X = np.random.randn(n_samples, n_features)
        
        if model_type == 'classification':
            # Generate binary classification target
            y = (X[:, 0] + X[:, 1] + np.random.randn(n_samples) * 0.1) > 0
            y = y.astype(int)
        else:
            # Generate regression target
            y = X[:, 0] * 2 + X[:, 1] * 1.5 + np.random.randn(n_samples) * 0.5
        
        return X, y
    
    def _get_feature_importance(self, model_name: str) -> Dict[str, float]:
        """Get feature importance if available"""
        
        model = self.models[model_name]
        
        if hasattr(model, 'feature_importances_'):
            n_features = len(model.feature_importances_)
            return {
                f'feature_{i+1}': round(float(importance), 4)
                for i, importance in enumerate(model.feature_importances_)
            }
        elif hasattr(model, 'coef_'):
            n_features = len(model.coef_) if model.coef_.ndim == 1 else len(model.coef_[0])
            coef = model.coef_ if model.coef_.ndim == 1 else model.coef_[0]
            return {
                f'feature_{i+1}': round(float(coef_val), 4)
                for i, coef_val in enumerate(coef)
            }
        else:
            return {'message': 'Feature importance not available for this model type'}
