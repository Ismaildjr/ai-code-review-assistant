#!/usr/bin/env python3
"""
Simple test client for the Static Code Analysis API.
Demonstrates how to use the API endpoints.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint."""
    print("🔍 Testing health endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Version: {data['version']}")
            print(f"   Timestamp: {data['timestamp']}")
            print(f"   Tools available: {list(data['tools_available'].keys())}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running.")
        return False
    
    return True

def test_tools_endpoint():
    """Test the tools information endpoint."""
    print("\n🔍 Testing tools endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/tools")
        if response.status_code == 200:
            data = response.json()
            print("✅ Tools endpoint working:")
            for tool_name, tool_info in data['tools'].items():
                print(f"   {tool_info['name']}: {tool_info['description']}")
        else:
            print(f"❌ Tools endpoint failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API.")
        return False
    
    return True

def test_analyze_endpoint():
    """Test the main analysis endpoint."""
    print("\n🔍 Testing analyze endpoint...")
    
    # Sample Python code with various issues
    sample_code = '''
import os
import subprocess
import pickle

def bad_function(  x,y  ):
    """Function with formatting issues."""
    z=x+y
    print(z)
    return z

def unsafe_function():
    """Function with security issues."""
    user_input = input("Enter command: ")
    os.system(user_input)  # Security issue
    exec(user_input)       # Security issue
    return "unsafe"

def complex_function(n):
    """Function with high complexity."""
    if n < 0:
        return -1
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        result = 0
        for i in range(n):
            if i % 2 == 0:
                result += i
            else:
                result -= i
        return result

class SampleClass:
    """Sample class for analysis."""
    def __init__(self):
        self.value = 0
    
    def get_value(self):
        return self.value
'''
    
    request_data = {
        "code": sample_code,
        "filename": "sample.py",
        "include_tools": ["pylint", "flake8", "radon", "bandit"]
    }
    
    try:
        print("   Sending analysis request...")
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            execution_time = time.time() - start_time
            
            print(f"✅ Analysis completed in {execution_time:.2f}s")
            print(f"   API execution time: {data['execution_time_ms']:.2f}ms")
            print(f"   Success: {data['success']}")
            print(f"   Filename: {data['filename']}")
            
            # Print summary
            summary = data['summary']
            print(f"\n📊 Analysis Summary:")
            print(f"   Total issues: {summary['total_issues']}")
            print(f"   Total functions: {summary['total_functions']}")
            print(f"   Total classes: {summary['total_classes']}")
            print(f"   Security issues: {summary['security_issues']}")
            print(f"   Style issues: {summary['style_issues']}")
            print(f"   Quality issues: {summary['quality_issues']}")
            print(f"   Complexity issues: {summary['complexity_issues']}")
            print(f"   Tools executed: {summary['tools_executed']}")
            print(f"   Tools failed: {summary['tools_failed']}")
            
            # Print detailed results
            print(f"\n🔧 Detailed Results:")
            for tool_name, tool_results in data['results'].items():
                if tool_results.get('success'):
                    tool_summary = tool_results.get('summary', {})
                    if 'total_issues' in tool_summary:
                        print(f"   {tool_name.capitalize()}: {tool_summary['total_issues']} issues")
                    elif 'total_functions' in tool_summary:
                        print(f"   {tool_name.capitalize()}: {tool_summary['total_functions']} functions analyzed")
                else:
                    print(f"   {tool_name.capitalize()}: Failed - {tool_results.get('error', 'Unknown error')}")
            
            # Print any errors
            if data['errors']:
                print(f"\n⚠️  Errors encountered:")
                for error in data['errors']:
                    print(f"   {error}")
                    
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API.")
        return False
    except Exception as e:
        print(f"❌ Analysis request failed: {str(e)}")
        return False
    
    return True

def test_partial_analysis():
    """Test analysis with only specific tools."""
    print("\n🔍 Testing partial analysis (radon + bandit only)...")
    
    sample_code = '''
def simple_function():
    return 42

def complex_function(n):
    if n < 0:
        return -1
    elif n == 0:
        return 0
    else:
        result = 0
        for i in range(n):
            if i % 2 == 0:
                result += i
        return result
'''
    
    request_data = {
        "code": sample_code,
        "include_tools": ["radon", "bandit"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=request_data)
        if response.status_code == 200:
            data = response.json()
            results = data['results']
            
            print("✅ Partial analysis completed:")
            print(f"   Tools requested: {request_data['include_tools']}")
            print(f"   Tools executed: {data['summary']['tools_executed']}")
            print(f"   Results keys: {list(results.keys())}")
            
            # Verify only requested tools were executed
            for tool in ["pylint", "flake8"]:
                if tool in results:
                    print(f"   ⚠️  Warning: {tool} was executed but not requested")
            
        else:
            print(f"❌ Partial analysis failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Partial analysis failed: {str(e)}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Static Code Analysis API Test Client")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("\n❌ API server is not running. Please start it first:")
        print("   python api.py")
        return
    
    # Test tools endpoint
    test_tools_endpoint()
    
    # Test main analysis endpoint
    test_analyze_endpoint()
    
    # Test partial analysis
    test_partial_analysis()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()
