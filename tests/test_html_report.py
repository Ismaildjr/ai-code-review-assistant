#!/usr/bin/env python3
"""
Test script for the Professional HTML Report Generator.
Demonstrates how to generate beautiful, client-ready HTML reports.
"""

import requests
import os
import webbrowser
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
HF_TOKEN = os.getenv("HF_TOKEN")

def test_html_report_generation():
    """Test HTML report generation with professional branding."""
    print("=== Testing Professional HTML Report Generation ===")
    
    # Sample code with various issues for demonstration
    code = """
import os
import subprocess
import pickle
import yaml

def calculate_sum(a, b):
    """Calculate sum of two numbers."""
    result = a + b
    return result

def very_long_function(a,b,c,d,e,f,g,h,i,j):
    """Function with too many parameters."""
    print("This function has too many parameters")
    temp_result = 0
    for param in [a,b,c,d,e,f,g,h,i,j]:
        temp_result += param
    return temp_result

def unsafe_function():
    """Function with security vulnerabilities."""
    user_input = input("Enter command: ")
    
    # Security issue: os.system with user input
    os.system(user_input)  # B101: use of os.system
    
    # Security issue: exec with user input
    exec(user_input)  # B102: use of exec
    
    # Security issue: unsafe file permissions
    os.chmod("/tmp/file", 0o777)  # B103: use of set_bad_file_permissions
    
    # Security issue: pickle with user input
    data = pickle.loads(user_input)  # B301: use of pickle
    
    # Security issue: yaml.load with user input
    config = yaml.load(user_input)  # B506: use of yaml.load
    
    return "unsafe"

def safe_function():
    """Function with safe practices."""
    # Safe alternatives
    result = subprocess.run(['ls'], capture_output=True, text=True)
    
    # Safe file permissions
    os.chmod("/tmp/file", 0o600)
    
    # Safe YAML loading
    config = yaml.safe_load("safe: true")
    
    return "safe"

class DataProcessor:
    """Class for processing data."""
    
    def __init__(self):
        self.data = []
    
    def add_item(self, item):
        """Add item to data."""
        self.data.append(item)
    
    def process_data(self):
        """Process all data items."""
        processed = []
        for item in self.data:
            if item is not None:
                processed.append(item * 2)
        return processed

# Main execution
if __name__ == "__main__":
    processor = DataProcessor()
    processor.add_item(5)
    processor.add_item(10)
    result = processor.process_data()
    print(f"Processed result: {result}")
"""
    
    try:
        print("🔄 Generating professional HTML report...")
        
        # Generate HTML report with custom branding
        response = requests.post(
            f"{API_BASE_URL}/report/html",
            data=code,
            headers={"Content-Type": "text/plain"},
            params={
                "filename": "sample_code.py",
                "include_tools": "pylint,flake8,radon,bandit",
                "llm_provider": "huggingface",
                "company_name": "Elite Code Review Services",
                "logo_url": "https://via.placeholder.com/80x80/667eea/ffffff?text=ECR"
            }
        )
        
        if response.status_code == 200:
            print("✅ HTML report generated successfully!")
            
            # Save the HTML report
            timestamp = os.popen('date +%Y%m%d_%H%M%S').read().strip()
            report_filename = f"professional_code_review_{timestamp}.html"
            
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"📄 Report saved as: {report_filename}")
            
            # Get report metadata from headers
            report_id = response.headers.get('X-Report-ID', 'Unknown')
            execution_time = response.headers.get('X-Execution-Time', 'Unknown')
            
            print(f"🆔 Report ID: {report_id}")
            print(f"⏱️  Generation time: {execution_time}")
            
            # Try to open the report in browser
            try:
                print("🌐 Opening report in browser...")
                webbrowser.open(f"file://{os.path.abspath(report_filename)}")
            except Exception as e:
                print(f"⚠️  Could not open browser automatically: {e}")
                print(f"   Please open {report_filename} manually in your browser")
            
            return report_filename
            
        else:
            print(f"❌ Report generation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_html_report_generator_directly():
    """Test the HTML report generator directly without API."""
    print("\n=== Testing HTML Report Generator Directly ===")
    
    try:
        from html_report_generator import create_report_generator
        
        # Create generator with custom branding
        generator = create_report_generator(
            company_name="Direct Test Company",
            logo_url="https://via.placeholder.com/80x80/48bb78/ffffff?text=DT"
        )
        
        # Sample analysis results
        sample_results = {
            "summary": {
                "total_issues": 12,
                "security_issues": 3,
                "style_issues": 6,
                "quality_issues": 2,
                "complexity_issues": 1,
                "tools_executed": 4
            },
            "pylint": {
                "success": True,
                "summary": {"total_issues": 4},
                "issues": [
                    {"message": "Function name should be snake_case"},
                    {"message": "Unused variable 'temp_result'"},
                    {"message": "Missing docstring"},
                    {"message": "Too many arguments"}
                ]
            },
            "flake8": {
                "success": True,
                "summary": {"total_issues": 2},
                "issues": [
                    {"message": "E501 line too long (120 > 79 characters)"},
                    {"message": "E302 expected 2 blank lines"}
                ]
            },
            "radon": {
                "success": True,
                "summary": {"total_functions": 4, "complexity_issues": 1}
            },
            "bandit": {
                "success": True,
                "summary": {"total_issues": 3, "high_severity": 2},
                "results": {
                    "results": [
                        {
                            "issue_severity": "HIGH",
                            "issue_text": "Use of os.system with user input"
                        },
                        {
                            "issue_severity": "HIGH", 
                            "issue_text": "Use of exec with user input"
                        },
                        {
                            "issue_severity": "MEDIUM",
                            "issue_text": "Use of pickle.loads"
                        }
                    ]
                }
            },
            "ai_review": {
                "success": True,
                "review": """This code demonstrates several areas that need attention:

**Security Issues (Critical Priority):**
- The `unsafe_function()` contains multiple security vulnerabilities including command injection via `os.system()` and `exec()`
- Use of `pickle.loads()` with user input can lead to code execution attacks
- Unsafe file permissions (0o777) expose files to all users

**Code Style Issues (Medium Priority):**
- Function naming should follow snake_case convention
- Some functions are missing proper docstrings
- Line length exceeds PEP 8 recommendations

**Code Quality Issues (Low Priority):**
- The `very_long_function()` has too many parameters (10) - consider using a data structure
- Unused variables should be removed

**Recommendations:**
1. Replace `os.system()` with `subprocess.run()` for safe command execution
2. Avoid `exec()` and `pickle.loads()` with untrusted input
3. Use `yaml.safe_load()` instead of `yaml.load()`
4. Refactor long parameter lists into configuration objects
5. Add comprehensive docstrings to all functions""",
                "provider": "huggingface",
                "execution_time_ms": 3200
            }
        }
        
        sample_code = """
def calculateSum(a, b):
    temp = a + b
    return temp

def very_long_function(a,b,c,d,e,f,g,h,i,j):
    print("This is too long")
    return a+b+c+d+e+f+g+h+i+j

def unsafe_function():
    user_input = input("Enter command: ")
    os.system(user_input)  # Security issue
    return "unsafe"
"""
        
        # Generate and save report
        output_file = generator.save_report(sample_results, sample_code, "test_code.py")
        print(f"✅ Direct report generated: {output_file}")
        
        # Try to open in browser
        try:
            webbrowser.open(f"file://{os.path.abspath(output_file)}")
            print("🌐 Report opened in browser")
        except:
            print(f"📄 Report saved at: {output_file}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error testing direct generator: {str(e)}")
        return None

def main():
    """Main test function."""
    print("🚀 Testing Professional HTML Report Generation")
    print("=" * 60)
    
    if not HF_TOKEN:
        print("⚠️  Warning: HF_TOKEN environment variable not set")
        print("   AI review functionality may not work without proper authentication")
        print()
    
    # Test 1: API-based HTML report generation
    api_report = test_html_report_generation()
    
    # Test 2: Direct HTML report generation
    direct_report = test_html_report_generator_directly()
    
    print("\n🎉 Testing completed!")
    
    if api_report or direct_report:
        print("\n📋 Generated Reports:")
        if api_report:
            print(f"   • API Report: {api_report}")
        if direct_report:
            print(f"   • Direct Report: {direct_report}")
        
        print("\n💡 Tips:")
        print("   • Open the HTML files in your browser to view the reports")
        print("   • Reports are fully responsive and print-friendly")
        print("   • Customize company name and logo for branding")
        print("   • Perfect for client delivery and professional presentations")

if __name__ == "__main__":
    main()
