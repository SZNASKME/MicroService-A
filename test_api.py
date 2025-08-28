# Example API usage for Data Analytics Microservice

import requests
import json

# Base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_descriptive_analysis():
    """Test descriptive analysis"""
    data = {
        "columns": ["revenue", "profit", "customers", "orders"],
        "analysis_params": {
            "include_outliers": True,
            "confidence_level": 0.95
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/analysis/descriptive",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print("Descriptive Analysis:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_correlation_analysis():
    """Test correlation analysis"""
    data = {
        "columns": ["revenue", "profit", "customers"],
        "method": "pearson",
        "significance_threshold": 0.5
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/analysis/correlation",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print("Correlation Analysis:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_visualization():
    """Test chart generation"""
    data = {
        "chart_type": "bar",
        "config": {
            "title": "Sales Performance",
            "width": 800,
            "height": 600,
            "data_points": 12,
            "color_scheme": "default"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/visualization/chart",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print("Chart Generation:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_ml_training():
    """Test ML model training"""
    data = {
        "model_type": "classification",
        "algorithm": "random_forest",
        "model_name": "sales_predictor",
        "n_samples": 1000,
        "n_features": 10,
        "test_size": 0.2,
        "cv_folds": 5
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/ml/train",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print("ML Model Training:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_data_validation():
    """Test data quality validation"""
    data = {
        "columns": ["customer_id", "order_date", "amount", "status"],
        "validation_level": "comprehensive"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/validation/quality",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print("Data Quality Validation:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_report_generation():
    """Test report generation"""
    data = {
        "report_type": "detailed_analysis",
        "include_sections": ["summary", "analysis", "visualizations", "recommendations"],
        "date_range": {
            "start": "2024-01-01T00:00:00",
            "end": "2024-01-31T23:59:59"
        },
        "data_sources": ["sales_database", "customer_api"]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/reports/generate",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print("Report Generation:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_dashboard_creation():
    """Test dashboard creation"""
    data = {
        "dashboard_config": {
            "title": "Sales Analytics Dashboard",
            "theme": "light",
            "layout": "grid"
        },
        "charts": [
            {
                "type": "line",
                "title": "Revenue Trend",
                "data_points": 12
            },
            {
                "type": "bar",
                "title": "Product Sales",
                "data_points": 8
            },
            {
                "type": "pie",
                "title": "Market Share",
                "data_points": 5
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/visualization/dashboard",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print("Dashboard Creation:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

if __name__ == "__main__":
    print("Testing Data Analytics Microservice API\n")
    print("=" * 60)
    
    try:
        # Test all endpoints
        test_health_check()
        test_descriptive_analysis()
        test_correlation_analysis()
        test_visualization()
        test_ml_training()
        test_data_validation()
        test_report_generation()
        test_dashboard_creation()
        
        print("All tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the microservice.")
        print("Please make sure the service is running on http://localhost:5000")
    except Exception as e:
        print(f"Error occurred during testing: {e}")
