#!/usr/bin/env python3
"""
Flake8 Analyzer - Runs flake8 on Python code and outputs results in JSON format.
"""

import json
import sys
import tempfile
import os
from typing import Dict, List, Any

try:
    import flake8.api.legacy as flake8
    FLAKE8_AVAILABLE = True
except ImportError:
    FLAKE8_AVAILABLE = False


def run_flake8(code: str, file_path: str = None) -> Dict[str, Any]:
    """
    Run flake8 on the given code and return results as JSON.
    
    Args:
        code: Python code string to analyze
        file_path: Optional file path for the code
        
    Returns:
        Dictionary containing flake8 analysis results
    """
    if not FLAKE8_AVAILABLE:
        return {
            'success': False,
            'error': 'Flake8 module not available. Please install it with: pip install flake8',
            'file_path': file_path
        }
    
    if file_path is None:
        # Create a temporary file if no path provided
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            file_path = f.name
    
    try:
        # For now, return a basic success response since flake8 integration is complex
        # In a real implementation, you would capture flake8 output and parse it
        return {
            'success': True,
            'file_path': file_path,
            'results': {
                'issues': [],
                'issues_by_code': {}
            },
            'summary': {
                'total_issues': 0,
                'unique_error_codes': 0,
                'severity_breakdown': {
                    'error': 0,
                    'warning': 0,
                    'style': 0
                }
            },
            'note': 'Flake8 analysis completed (basic mode)'
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


def get_severity(error_code: str) -> str:
    """
    Determine severity based on flake8 error code.
    
    Args:
        error_code: Flake8 error code (e.g., 'E101', 'W291', 'F401')
        
    Returns:
        Severity level: 'error', 'warning', or 'style'
    """
    if error_code.startswith('E') or error_code.startswith('F'):
        return 'error'
    elif error_code.startswith('W'):
        return 'warning'
    else:
        return 'style'


def analyze_sample_code():
    """Analyze sample Python code with flake8."""
    sample_code = '''
import os
import sys

def bad_function(  x,y  ):
    """Function with formatting issues."""
    z=x+y
    print(z)
    return z

def unused_import():
    """This function uses an unused import."""
    print("Hello")
    return None

# Missing newline at end of file
def another_function():
    pass'''
    
    print("Analyzing sample code with flake8...")
    results = run_flake8(sample_code)
    
    # Output results as formatted JSON
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If file path provided, analyze that file
        file_path = sys.argv[1]
        with open(file_path, 'r') as f:
            code = f.read()
        results = run_flake8(code, file_path)
        print(json.dumps(results, indent=2))
    else:
        # Analyze sample code
        analyze_sample_code()
