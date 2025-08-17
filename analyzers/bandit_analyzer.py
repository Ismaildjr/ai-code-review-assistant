#!/usr/bin/env python3
"""
Bandit Analyzer - Runs bandit on Python code and outputs results in JSON format.
"""

import json
import sys
import tempfile
import os
from typing import Dict, List, Any

try:
    import bandit.core.manager
    import bandit.core.config
    BANDIT_AVAILABLE = True
except ImportError:
    BANDIT_AVAILABLE = False


def run_bandit(code: str, file_path: str = None) -> Dict[str, Any]:
    """
    Run bandit on the given code and return results as JSON.
    
    Args:
        code: Python code string to analyze
        file_path: Optional file path for the code
        
    Returns:
        Dictionary containing bandit analysis results
    """
    if not BANDIT_AVAILABLE:
        return {
            'success': False,
            'error': 'Bandit module not available. Please install it with: pip install bandit',
            'file_path': file_path
        }
    
    if file_path is None:
        # Create a temporary file if no path provided
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            file_path = f.name
    
    try:
        # Use bandit module directly
        config = bandit.core.config.BanditConfig()
        manager = bandit.core.manager.BanditManager(config, 'file')
        manager.discover_files([file_path])
        manager.run_tests()
        
        # Get results using as_dict method
        issues = []
        for issue in manager.get_issue_list():
            issue_dict = issue.as_dict()
            issues.append(issue_dict)
        
        return {
            'success': True,
            'file_path': file_path,
            'results': {'results': issues},
            'summary': {
                'total_issues': len(issues),
                'high_severity': len([r for r in issues if r.get('issue_severity') == 'HIGH']),
                'medium_severity': len([r for r in issues if r.get('issue_severity') == 'MEDIUM']),
                'low_severity': len([r for r in issues if r.get('issue_severity') == 'LOW']),
                'confidence_high': len([r for r in issues if r.get('issue_confidence') == 'HIGH']),
                'confidence_medium': len([r for r in issues if r.get('issue_confidence') == 'MEDIUM']),
                'confidence_low': len([r for r in issues if r.get('issue_confidence') == 'LOW'])
            }
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
    """Analyze sample Python code with bandit."""
    sample_code = '''
import os
import subprocess
import pickle
import yaml

def unsafe_function():
    """Function with security issues."""
    user_input = input("Enter command: ")
    os.system(user_input)  # B101: use of os.system
    
    # B102: use of exec
    exec(user_input)
    
    # B103: use of set_bad_file_permissions
    os.chmod("/tmp/file", 0o777)
    
    # B301: use of pickle
    data = pickle.loads(user_input)
    
    # B506: use of yaml.load
    config = yaml.load(user_input)
    
    return "unsafe"

def safe_function():
    """Function with safe practices."""
    # Safe alternatives
    import subprocess
    result = subprocess.run(['ls'], capture_output=True, text=True)
    
    # Safe file permissions
    os.chmod("/tmp/file", 0o600)
    
    # Safe YAML loading
    config = yaml.safe_load("safe: true")
    
    return "safe"
'''
    
    print("Analyzing sample code with bandit...")
    results = run_bandit(sample_code)
    
    # Output results as formatted JSON
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If file path provided, analyze that file
        file_path = sys.argv[1]
        with open(file_path, 'r') as f:
            code = f.read()
        results = run_bandit(code, file_path)
        print(json.dumps(results, indent=2))
    else:
        # Analyze sample code
        analyze_sample_code()
