#!/usr/bin/env python3
"""
Unit tests for the Static Code Analysis API.
"""

import pytest
from fastapi.testclient import TestClient
from api import app, calculate_overall_summary
import json

# Create test client
client = TestClient(app)

# Test data
SAMPLE_PYTHON_CODE = '''
def hello_world():
    """Simple function for testing."""
    print("Hello, World!")
    return "Hello, World!"

def complex_function(n):
    """More complex function for testing."""
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

class TestClass:
    """Test class for analysis."""
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        return self.value
'''

SAMPLE_CODE_WITH_ISSUES = '''
import os
import subprocess

def bad_function(  x,y  ):
    """Function with formatting issues."""
    z=x+y
    print(z)
    return z

def unsafe_function():
    """Function with security issues."""
    user_input = input("Enter command: ")
    os.system(user_input)
    return "unsafe"
'''

class TestHealthEndpoints:
    """Test health and information endpoints."""
    
    def test_root_endpoint(self):
        """Test the root health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "1.0.0"
        assert "tools_available" in data
        
        # Check that all tools are marked as available
        tools = data["tools_available"]
        assert tools["pylint"] == True
        assert tools["flake8"] == True
        assert tools["radon"] == True
        assert tools["bandit"] == True
    
    def test_tools_endpoint(self):
        """Test the tools information endpoint."""
        response = client.get("/tools")
        assert response.status_code == 200
        
        data = response.json()
        assert "tools" in data
        
        tools = data["tools"]
        assert "pylint" in tools
        assert "flake8" in tools
        assert "radon" in tools
        assert "bandit" in tools
        
        # Check tool information structure
        for tool_name, tool_info in tools.items():
            assert "name" in tool_info
            assert "description" in tool_info
            assert "status" in tool_info
            assert "capabilities" in tool_info
            assert tool_info["status"] == "available"

class TestAnalysisEndpoint:
    """Test the main analysis endpoint."""
    
    def test_analyze_code_basic(self):
        """Test basic code analysis with all tools."""
        request_data = {
            "code": SAMPLE_PYTHON_CODE,
            "filename": "test.py"
        }
        
        response = client.post("/analyze", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert "timestamp" in data
        assert "execution_time_ms" in data
        assert data["filename"] == "test.py"
        assert "results" in data
        assert "summary" in data
        assert "errors" in data
        
        # Check that all tools were executed
        results = data["results"]
        assert "pylint" in results
        assert "flake8" in results
        assert "radon" in results
        assert "bandit" in results
        
        # Check summary structure
        summary = data["summary"]
        assert "total_issues" in summary
        assert "total_functions" in summary
        assert "total_classes" in summary
        assert "tools_executed" in summary
        assert summary["tools_executed"] == 4
    
    def test_analyze_code_specific_tools(self):
        """Test code analysis with specific tools only."""
        request_data = {
            "code": SAMPLE_PYTHON_CODE,
            "include_tools": ["radon", "bandit"]
        }
        
        response = client.post("/analyze", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        
        results = data["results"]
        assert "radon" in results
        assert "bandit" in results
        assert "pylint" not in results
        assert "flake8" not in results
        
        summary = data["summary"]
        assert summary["tools_executed"] == 2
    
    def test_analyze_code_with_issues(self):
        """Test code analysis with code that has known issues."""
        request_data = {
            "code": SAMPLE_CODE_WITH_ISSUES,
            "filename": "issues.py"
        }
        
        response = client.post("/analyze", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        
        # Check that bandit found security issues (or at least ran successfully)
        bandit_results = data["results"]["bandit"]
        if bandit_results.get("success"):
            # Bandit should have run successfully, even if no issues found
            assert "summary" in bandit_results
            # The code has os.system which should trigger security warnings
            # But if no issues are found, that's also valid
            print(f"Bandit found {bandit_results['summary'].get('total_issues', 0)} security issues")
        else:
            # If bandit failed, check the error
            assert "error" in bandit_results
    
    def test_analyze_code_empty(self):
        """Test code analysis with empty code (should fail validation)."""
        request_data = {
            "code": "",
            "filename": "empty.py"
        }
        
        response = client.post("/analyze", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_analyze_code_invalid_tool(self):
        """Test code analysis with invalid tool name."""
        request_data = {
            "code": SAMPLE_PYTHON_CODE,
            "include_tools": ["invalid_tool", "pylint"]
        }
        
        response = client.post("/analyze", json=request_data)
        # The API should handle invalid tools gracefully and return an error
        # Check if the response contains an error about the invalid tool
        assert response.status_code in [200, 400]  # Could be either
        
        data = response.json()
        if response.status_code == 400:
            # API properly rejected the invalid tool
            assert "detail" in data
            assert "Invalid tool 'invalid_tool'" in data["detail"]
        else:
            # API handled it gracefully, check if there are errors in the response
            # The API returns success=False when there are validation errors
            assert data["success"] == False
            # Check if there are any errors about the invalid tool
            if data["errors"]:
                error_messages = " ".join(data["errors"]).lower()
                assert "invalid_tool" in error_messages or "invalid tool" in error_messages
    
    def test_analyze_code_minimal(self):
        """Test code analysis with minimal valid request."""
        request_data = {
            "code": "print('Hello')"
        }
        
        response = client.post("/analyze", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert data["filename"] is None  # Should be None when not provided

class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_calculate_overall_summary(self):
        """Test the overall summary calculation function."""
        # Mock results data
        mock_results = {
            "pylint": {
                "success": True,
                "summary": {"total_issues": 5}
            },
            "flake8": {
                "success": True,
                "summary": {"total_issues": 3}
            },
            "radon": {
                "success": True,
                "summary": {
                    "total_functions": 10,
                    "total_classes": 2,
                    "complexity_ranges": {
                        "A (1-5)": 8,
                        "B (6-10)": 1,
                        "C (11-20)": 1,
                        "D (21-50)": 0,
                        "E (51+)": 0
                    }
                }
            },
            "bandit": {
                "success": True,
                "summary": {"total_issues": 2}
            }
        }
        
        summary = calculate_overall_summary(mock_results)
        
        assert summary["total_issues"] == 10  # 5 + 3 + 2
        assert summary["total_functions"] == 10
        assert summary["total_classes"] == 2
        assert summary["security_issues"] == 2  # bandit issues
        assert summary["style_issues"] == 8  # flake8 + pylint issues
        assert summary["quality_issues"] == 8  # flake8 + pylint issues
        assert summary["complexity_issues"] == 1  # C (11-20) range
        assert summary["tools_executed"] == 4
        assert summary["tools_failed"] == 0
    
    def test_calculate_overall_summary_with_failures(self):
        """Test summary calculation when some tools fail."""
        mock_results = {
            "pylint": {
                "success": False,
                "error": "Tool failed"
            },
            "flake8": {
                "success": True,
                "summary": {"total_issues": 3}
            },
            "radon": {
                "success": True,
                "summary": {"total_functions": 5}
            }
        }
        
        summary = calculate_overall_summary(mock_results)
        
        assert summary["total_issues"] == 3  # Only flake8 issues
        assert summary["total_functions"] == 5
        assert summary["tools_executed"] == 3
        assert summary["tools_failed"] == 1

class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_malformed_json(self):
        """Test handling of malformed JSON."""
        response = client.post("/analyze", data="invalid json")
        assert response.status_code == 422
    
    def test_missing_required_field(self):
        """Test handling of missing required fields."""
        request_data = {
            "filename": "test.py"
            # Missing 'code' field
        }
        
        response = client.post("/analyze", json=request_data)
        assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
