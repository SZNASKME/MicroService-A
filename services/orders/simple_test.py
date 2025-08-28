import requests
import json

def test_health():
    try:
        response = requests.get('http://localhost:5000/health')
        print("Health Check Response:")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"Error testing health endpoint: {e}")
        return False

def test_descriptive_analysis():
    try:
        data = {
            "columns": ["revenue", "profit", "customers"],
        }
        response = requests.post(
            'http://localhost:5000/api/v1/analysis/descriptive',
            json=data
        )
        print("\nDescriptive Analysis Response:")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"Error testing descriptive analysis: {e}")
        return False

if __name__ == "__main__":
    print("Testing Data Analytics Microservice...\n")
    
    success = test_health()
    if success:
        success = test_descriptive_analysis()
    
    if success:
        print("\n✅ Tests completed successfully!")
    else:
        print("\n❌ Some tests failed.")
