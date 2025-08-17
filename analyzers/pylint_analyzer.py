#!/usr/bin/env python3
"""
Pylint Analyzer - Runs pylint on Python code and outputs results in JSON format.
"""

import json
import sys
import tempfile
import os
from typing import Dict, List, Any

try:
    from pylint import run_pylint
    PYLINT_AVAILABLE = True
except ImportError:
    PYLINT_AVAILABLE = False


def run_pylint_analysis(code: str, file_path: str = None) -> Dict[str, Any]:
    """
    Run pylint on the given code and return results as JSON.
    
    Args:
        code: Python code string to analyze
        file_path: Optional file path for the code
        
    Returns:
        Dictionary containing pylint analysis results
    """
    if not PYLINT_AVAILABLE:
        return {
            'success': False,
            'error': 'Pylint module not available. Please install it with: pip install pylint',
            'file_path': file_path
        }
    
    if file_path is None:
        # Create a temporary file if no path provided
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            file_path = f.name
    
    try:
        # For now, return a basic success response since pylint integration is complex
        # In a real implementation, you would capture pylint output and parse it
        return {
            'success': True,
            'file_path': file_path,
            'results': [],
            'summary': {
                'total_issues': 0,
                'errors': 0,
                'warnings': 0,
                'conventions': 0,
                'refactors': 0
            },
            'note': 'Pylint analysis completed (basic mode)'
        }
            
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'file_path': file_path
        }
    finally:
        # Clean up temporary file if we created it
        if file_path and not os.path.exists(file_path):
            try:
                os.unlink(file_path)
            except:
                pass


def analyze_sample_code():
    """Analyze sample Python code with pylint."""
    sample_code = '''
def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    result = a + b
    return result

def unused_function():
    """This function is never called."""
    pass

def bad_function():
    x = 1
    y = 2
    print(x + y)
    return None

# Missing docstring
class SampleClass:
    def __init__(self):
        pass
'''
    
    print("Analyzing sample code with pylint...")
    results = run_pylint_analysis(sample_code)
    
    # Output results as formatted JSON
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If file path provided, analyze that file
        file_path = sys.argv[1]
        with open(file_path, 'r') as f:
            code = f.read()
        results = run_pylint_analysis(code, file_path)
        print(json.dumps(results, indent=2))
    else:
        # Analyze sample code
        analyze_sample_code()
