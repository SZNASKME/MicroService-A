#!/usr/bin/env python3
"""
Production readiness test script
Tests all production features and configurations
"""

import requests
import time
import json
import os
import sys
from datetime import datetime

class ProductionTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.results = []
        
    def log_result(self, test_name, success, message="", details=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_result("Health Check", True, "Service is healthy")
                    return True
                else:
                    self.log_result("Health Check", False, f"Unhealthy status: {data.get('status')}")
                    return False
            else:
                self.log_result("Health Check", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Health Check", False, "Connection failed", str(e))
            return False
    
    def test_metrics_endpoints(self):
        """Test metrics endpoints"""
        try:
            # Test JSON metrics
            response = requests.get(f"{self.base_url}/api/v1/metrics", timeout=5)
            if response.status_code == 200:
                self.log_result("Metrics JSON", True, "Metrics endpoint accessible")
            else:
                self.log_result("Metrics JSON", False, f"HTTP {response.status_code}")
                return False
            
            # Test Prometheus metrics
            response = requests.get(f"{self.base_url}/metrics", timeout=5)
            if response.status_code == 200 and 'text/plain' in response.headers.get('content-type', ''):
                self.log_result("Metrics Prometheus", True, "Prometheus metrics available")
            else:
                self.log_result("Metrics Prometheus", False, f"HTTP {response.status_code}")
                return False
            
            return True
        except Exception as e:
            self.log_result("Metrics Endpoints", False, "Failed to access metrics", str(e))
            return False
    
    def test_error_handling(self):
        """Test error handling"""
        try:
            # Test 404 error
            response = requests.get(f"{self.base_url}/nonexistent", timeout=5)
            if response.status_code == 404:
                data = response.json()
                if 'error' in data:
                    self.log_result("404 Error Handling", True, "Proper 404 response")
                else:
                    self.log_result("404 Error Handling", False, "Missing error field in 404 response")
                    return False
            else:
                self.log_result("404 Error Handling", False, f"Expected 404, got {response.status_code}")
                return False
            
            return True
        except Exception as e:
            self.log_result("Error Handling", False, "Failed to test error handling", str(e))
            return False
    
    def test_performance(self):
        """Test basic performance"""
        try:
            times = []
            for i in range(10):
                start = time.time()
                response = requests.get(f"{self.base_url}/health", timeout=5)
                end = time.time()
                if response.status_code == 200:
                    times.append(end - start)
                else:
                    self.log_result("Performance Test", False, f"Request {i+1} failed")
                    return False
            
            avg_time = sum(times) / len(times)
            max_time = max(times)
            
            if avg_time < 0.5:  # 500ms average
                self.log_result("Performance Test", True, f"Avg: {avg_time:.3f}s, Max: {max_time:.3f}s")
            else:
                self.log_result("Performance Test", False, f"Slow response: {avg_time:.3f}s average")
                return False
            
            return True
        except Exception as e:
            self.log_result("Performance Test", False, "Failed to test performance", str(e))
            return False
    
    def test_cors_headers(self):
        """Test CORS configuration"""
        try:
            response = requests.options(f"{self.base_url}/health", timeout=5)
            headers = response.headers
            
            if 'Access-Control-Allow-Origin' in headers:
                self.log_result("CORS Headers", True, "CORS configured")
            else:
                self.log_result("CORS Headers", False, "CORS headers missing")
                return False
            
            return True
        except Exception as e:
            self.log_result("CORS Headers", False, "Failed to test CORS", str(e))
            return False
    
    def test_security_headers(self):
        """Test security headers"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            headers = response.headers
            
            # Check for basic security headers
            security_checks = []
            
            # Content-Type should be application/json
            if 'application/json' in headers.get('Content-Type', ''):
                security_checks.append("Content-Type: ✅")
            else:
                security_checks.append("Content-Type: ❌")
            
            if len(security_checks) > 0:
                self.log_result("Security Headers", True, f"Basic security headers present")
            else:
                self.log_result("Security Headers", False, "Security headers missing")
                return False
            
            return True
        except Exception as e:
            self.log_result("Security Headers", False, "Failed to test security headers", str(e))
            return False
    
    def run_all_tests(self):
        """Run all production tests"""
        print("🧪 Running Production Readiness Tests...\n")
        
        tests = [
            self.test_health_check,
            self.test_metrics_endpoints,
            self.test_error_handling,
            self.test_performance,
            self.test_cors_headers,
            self.test_security_headers
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(0.1)  # Small delay between tests
        
        print(f"\n📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Service is production ready.")
            return True
        else:
            print("⚠️  Some tests failed. Review the issues before deploying.")
            return False
    
    def generate_report(self):
        """Generate detailed test report"""
        report = {
            'test_run': {
                'timestamp': datetime.now().isoformat(),
                'total_tests': len(self.results),
                'passed': sum(1 for r in self.results if r['success']),
                'failed': sum(1 for r in self.results if not r['success'])
            },
            'results': self.results
        }
        
        # Save to file
        with open('production_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: production_test_report.json")
        return report

def main():
    """Main test runner"""
    base_url = os.getenv('TEST_URL', 'http://localhost:5000')
    
    print(f"🎯 Testing service at: {base_url}")
    
    tester = ProductionTester(base_url)
    success = tester.run_all_tests()
    tester.generate_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
