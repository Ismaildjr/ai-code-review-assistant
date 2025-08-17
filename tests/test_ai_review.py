#!/usr/bin/env python3
"""
Test script for the AI-powered code review functionality.
Demonstrates how to use the new endpoints.
"""

import requests
import json
import os

# Configuration
API_BASE_URL = "http://localhost:8000"
HF_TOKEN = os.getenv("HF_TOKEN")

def test_ai_review_with_json():
    """Test AI review using JSON endpoint."""
    print("=== Testing AI Review with JSON ===")
    
    code = """
def calculate_sum(a, b):
    return a + b

def very_long_function(a,b,c,d,e,f,g,h,i,j):
    print("This is too long")
    return a+b+c+d+e+f+g+h+i+j

def unsafe_function():
    user_input = input("Enter command: ")
    os.system(user_input)  # Security issue
    return "unsafe"
"""
    
    payload = {
        "code": code,
        "filename": "test_code.py",
        "include_tools": ["pylint", "flake8", "radon", "bandit"]
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/review", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI Review successful!")
            print(f"Execution time: {result['execution_time_ms']:.2f}ms")
            
            # Show AI review if available
            if 'ai_review' in result['results']:
                ai_review = result['results']['ai_review']
                if ai_review.get('success'):
                    print("\n🤖 AI Review Report:")
                    print("=" * 50)
                    print(ai_review['review'])
                else:
                    print(f"❌ AI Review failed: {ai_review.get('error')}")
            
            # Show summary
            print(f"\n📊 Summary:")
            print(f"Total issues: {result['summary'].get('total_issues', 0)}")
            print(f"Tools executed: {result['summary'].get('tools_executed', 0)}")
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_ai_review_with_plain_code():
    """Test AI review using plain code endpoint."""
    print("\n=== Testing AI Review with Plain Code ===")
    
    code = """
import os
import subprocess

def process_data(data):
    if data is None:
        return None
    
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    
    return result

def execute_command(cmd):
    os.system(cmd)  # Security vulnerability
    return True
"""
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/review/plain",
            data=code,
            headers={"Content-Type": "text/plain"},
            params={
                "filename": "plain_test.py",
                "include_tools": "pylint,flake8,radon,bandit",
                "llm_provider": "huggingface"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Plain Code AI Review successful!")
            print(f"Execution time: {result['execution_time_ms']:.2f}ms")
            
            # Show AI review if available
            if 'ai_review' in result['results']:
                ai_review = result['results']['ai_review']
                if ai_review.get('success'):
                    print("\n🤖 AI Review Report:")
                    print("=" * 50)
                    print(ai_review['review'])
                else:
                    print(f"❌ AI Review failed: {ai_review.get('error')}")
            
            # Show summary
            print(f"\n📊 Summary:")
            print(f"Total issues: {result['summary'].get('total_issues', 0)}")
            print(f"Security issues: {result['summary'].get('security_issues', 0)}")
            print(f"Style issues: {result['summary'].get('style_issues', 0)}")
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_health_check():
    """Test API health check."""
    print("=== Testing API Health Check ===")
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API is healthy!")
            print(f"Status: {result['status']}")
            print(f"Version: {result['version']}")
            print(f"Tools available: {list(result['tools_available'].keys())}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main test function."""
    print("🚀 Testing AI-Powered Code Review API")
    print("=" * 50)
    
    if not HF_TOKEN:
        print("⚠️  Warning: HF_TOKEN environment variable not set")
        print("   AI review functionality may not work without proper authentication")
        print()
    
    # Test health check first
    test_health_check()
    
    # Test AI review endpoints
    test_ai_review_with_json()
    test_ai_review_with_plain_code()
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    main()
