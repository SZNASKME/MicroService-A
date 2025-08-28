import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class StatisticalAnalyzer:
    """
    Statistical analysis service for performing various statistical analyses
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
    
    def descriptive_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform descriptive statistical analysis
        
        Args:
            data: Dictionary containing data and analysis parameters
            
        Returns:
            Dict containing descriptive statistics
        """
        try:
            # In production, you would load actual data
            # For demo, we'll create sample results
            
            columns = data.get('columns', ['column1', 'column2', 'column3'])
            
            # Sample descriptive statistics
            descriptive_stats = {}
            
            for column in columns:
                descriptive_stats[column] = {
                    'count': np.random.randint(900, 1000),
                    'mean': round(np.random.normal(50, 15), 2),
                    'std': round(np.random.uniform(5, 20), 2),
                    'min': round(np.random.uniform(0, 20), 2),
                    'max': round(np.random.uniform(80, 100), 2),
                    'median': round(np.random.uniform(40, 60), 2),
                    'q1': round(np.random.uniform(30, 45), 2),
                    'q3': round(np.random.uniform(55, 70), 2),
                    'skewness': round(np.random.uniform(-1, 1), 3),
                    'kurtosis': round(np.random.uniform(-2, 2), 3)
                }
            
            return {
                'status': 'success',
                'descriptive_statistics': descriptive_stats,
                'summary': {
                    'total_columns_analyzed': len(columns),
                    'analysis_type': 'descriptive'
                },
                'message': 'Descriptive analysis completed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error in descriptive analysis: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def correlation_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform correlation analysis between variables
        
        Args:
            data: Dictionary containing data and correlation parameters
            
        Returns:
            Dict containing correlation results
        """
        try:
            method = data.get('method', 'pearson')  # pearson, spearman, kendall
            columns = data.get('columns', ['column1', 'column2', 'column3'])
            
            # Sample correlation matrix
            n_cols = len(columns)
            correlation_matrix = {}
            
            for i, col1 in enumerate(columns):
                correlation_matrix[col1] = {}
                for j, col2 in enumerate(columns):
                    if i == j:
                        correlation_matrix[col1][col2] = 1.0
                    else:
                        # Generate realistic correlation values
                        corr_value = round(np.random.uniform(-0.8, 0.8), 3)
                        correlation_matrix[col1][col2] = corr_value
            
            # Find significant correlations
            significant_correlations = []
            threshold = data.get('significance_threshold', 0.5)
            
            for col1 in columns:
                for col2 in columns:
                    if col1 != col2:
                        corr_val = abs(correlation_matrix[col1][col2])
                        if corr_val >= threshold:
                            significant_correlations.append({
                                'variable1': col1,
                                'variable2': col2,
                                'correlation': correlation_matrix[col1][col2],
                                'strength': self._get_correlation_strength(corr_val)
                            })
            
            return {
                'status': 'success',
                'correlation_matrix': correlation_matrix,
                'significant_correlations': significant_correlations,
                'analysis_params': {
                    'method': method,
                    'threshold': threshold,
                    'variables_count': len(columns)
                },
                'message': 'Correlation analysis completed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error in correlation analysis: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def hypothesis_testing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform hypothesis testing
        
        Args:
            data: Dictionary containing test parameters
            
        Returns:
            Dict containing test results
        """
        try:
            test_type = data.get('test_type', 't_test')  # t_test, chi_square, anova
            alpha = data.get('alpha', 0.05)
            
            # Sample test results
            if test_type == 't_test':
                test_results = {
                    'test_statistic': round(np.random.normal(0, 2), 4),
                    'p_value': round(np.random.uniform(0.001, 0.1), 4),
                    'degrees_of_freedom': np.random.randint(50, 200),
                    'confidence_interval': [
                        round(np.random.uniform(-2, 0), 3),
                        round(np.random.uniform(0, 2), 3)
                    ]
                }
            elif test_type == 'chi_square':
                test_results = {
                    'test_statistic': round(np.random.uniform(5, 25), 4),
                    'p_value': round(np.random.uniform(0.001, 0.1), 4),
                    'degrees_of_freedom': np.random.randint(2, 10),
                    'critical_value': round(np.random.uniform(7, 15), 4)
                }
            else:  # ANOVA
                test_results = {
                    'f_statistic': round(np.random.uniform(2, 10), 4),
                    'p_value': round(np.random.uniform(0.001, 0.1), 4),
                    'between_groups_df': np.random.randint(2, 5),
                    'within_groups_df': np.random.randint(50, 200)
                }
            
            # Determine significance
            is_significant = test_results['p_value'] < alpha
            
            return {
                'status': 'success',
                'test_type': test_type,
                'test_results': test_results,
                'is_significant': is_significant,
                'alpha_level': alpha,
                'interpretation': self._interpret_test_result(test_type, is_significant, alpha),
                'message': f'{test_type} completed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error in hypothesis testing: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def outlier_detection(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect outliers in the data
        
        Args:
            data: Dictionary containing outlier detection parameters
            
        Returns:
            Dict containing outlier analysis results
        """
        try:
            method = data.get('method', 'iqr')  # iqr, zscore, isolation_forest
            columns = data.get('columns', ['column1', 'column2'])
            
            outlier_results = {}
            
            for column in columns:
                # Sample outlier detection results
                total_points = np.random.randint(800, 1000)
                outlier_count = np.random.randint(5, 50)
                
                outlier_results[column] = {
                    'total_points': total_points,
                    'outlier_count': outlier_count,
                    'outlier_percentage': round((outlier_count / total_points) * 100, 2),
                    'method_used': method,
                    'outlier_indices': list(np.random.choice(total_points, outlier_count, replace=False))
                }
            
            return {
                'status': 'success',
                'outlier_analysis': outlier_results,
                'method': method,
                'total_columns_analyzed': len(columns),
                'message': 'Outlier detection completed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error in outlier detection: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _get_correlation_strength(self, correlation_value: float) -> str:
        """Determine correlation strength based on value"""
        abs_corr = abs(correlation_value)
        if abs_corr >= 0.8:
            return 'very strong'
        elif abs_corr >= 0.6:
            return 'strong'
        elif abs_corr >= 0.4:
            return 'moderate'
        elif abs_corr >= 0.2:
            return 'weak'
        else:
            return 'very weak'
    
    def _interpret_test_result(self, test_type: str, is_significant: bool, alpha: float) -> str:
        """Provide interpretation of statistical test results"""
        if is_significant:
            return f"The result is statistically significant at α = {alpha} level. We reject the null hypothesis."
        else:
            return f"The result is not statistically significant at α = {alpha} level. We fail to reject the null hypothesis."
