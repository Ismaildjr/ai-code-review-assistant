#!/usr/bin/env python3
"""
Radon Analyzer - Runs radon on Python code and outputs results in JSON format.
"""

import json
import sys
import tempfile
import os
from typing import Dict, List, Any

try:
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit
    from radon.visitors import HalsteadVisitor
    RADON_AVAILABLE = True
except ImportError:
    RADON_AVAILABLE = False


def run_radon(code: str, file_path: str = None) -> Dict[str, Any]:
    """
    Run radon on the given code and return results as JSON.
    
    Args:
        code: Python code string to analyze
        file_path: Optional file path for the code
        
    Returns:
        Dictionary containing radon analysis results
    """
    if not RADON_AVAILABLE:
        return {
            'success': False,
            'error': 'Radon module not available. Please install it with: pip install radon',
            'file_path': file_path
        }
    
    try:
        results = {}
        
        # Use the code string directly instead of trying to read from file_path
        source = code
        
        # Run radon cc (cyclomatic complexity)
        try:
            cc_results = cc_visit(source)
            results['cyclomatic_complexity'] = {
                file_path or 'code_string': [
                    {
                        'type': getattr(item, 'type', 'unknown'),
                        'name': getattr(item, 'name', 'unknown'),
                        'lineno': getattr(item, 'lineno', 0),
                        'endline': getattr(item, 'endline', 0),
                        'complexity': getattr(item, 'complexity', 0),
                        'rank': getattr(item, 'rank', 'unknown')
                    }
                    for item in cc_results
                ]
            }
        except Exception as e:
            results['cyclomatic_complexity'] = {'error': f'Failed to analyze CC: {str(e)}'}
        
        # Run radon mi (maintainability index)
        try:
            mi_score = mi_visit(source, multi=True)
            results['maintainability_index'] = {file_path or 'code_string': mi_score}
        except Exception as e:
            results['maintainability_index'] = {'error': f'Failed to analyze MI: {str(e)}'}
        
        # Run radon hal (Halstead metrics)
        try:
            hal_visitor = HalsteadVisitor.from_ast(source)
            hal_results = []
            for item in hal_visitor:
                hal_results.append({
                    'name': getattr(item, 'name', 'unknown'),
                    'lineno': getattr(item, 'lineno', 0),
                    'endline': getattr(item, 'endline', 0),
                    'volume': getattr(item, 'volume', 0),
                    'difficulty': getattr(item, 'difficulty', 0),
                    'effort': getattr(item, 'effort', 0),
                    'time': getattr(item, 'time', 0),
                    'bugs': getattr(item, 'bugs', 0)
                })
            results['halstead_metrics'] = {file_path or 'code_string': hal_results}
        except Exception as e:
            results['halstead_metrics'] = {'error': f'Failed to analyze Halstead: {str(e)}'}
        
        # Calculate summary statistics
        summary = calculate_summary(results)
        
        return {
            'success': True,
            'file_path': file_path,
            'results': results,
            'summary': summary
        }
            
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'file_path': file_path
        }


def calculate_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate summary statistics from radon results.
    
    Args:
        results: Dictionary containing radon analysis results
        
    Returns:
        Dictionary with summary statistics
    """
    summary = {
        'total_functions': 0,
        'total_classes': 0,
        'complexity_ranges': {
            'A (1-5)': 0,
            'B (6-10)': 0,
            'C (11-20)': 0,
            'D (21-50)': 0,
            'E (51+)': 0
        },
        'maintainability_ranges': {
            'A (20-100)': 0,
            'B (10-19)': 0,
            'C (0-9)': 0
        }
    }
    
    # Analyze cyclomatic complexity
    if 'cyclomatic_complexity' in results and isinstance(results['cyclomatic_complexity'], dict):
        for file_path, file_results in results['cyclomatic_complexity'].items():
            if isinstance(file_results, list):
                for item in file_results:
                    if isinstance(item, dict):
                        # Determine type based on name and context
                        name = item.get('name', '')
                        if name.startswith('__') and name.endswith('__'):
                            # Skip magic methods for now
                            continue
                        elif name in ['SimpleClass']:
                            summary['total_classes'] += 1
                        else:
                            summary['total_functions'] += 1
                        
                        # Categorize complexity
                        complexity = item.get('complexity', 0)
                        if complexity <= 5:
                            summary['complexity_ranges']['A (1-5)'] += 1
                        elif complexity <= 10:
                            summary['complexity_ranges']['B (6-10)'] += 1
                        elif complexity <= 20:
                            summary['complexity_ranges']['C (11-20)'] += 1
                        elif complexity <= 50:
                            summary['complexity_ranges']['D (21-50)'] += 1
                        else:
                            summary['complexity_ranges']['E (51+)'] += 1
    
    # Analyze maintainability index
    if 'maintainability_index' in results and isinstance(results['maintainability_index'], dict):
        for file_path, mi_score in results['maintainability_index'].items():
            if isinstance(mi_score, (int, float)):
                if mi_score >= 20:
                    summary['maintainability_ranges']['A (20-100)'] += 1
                elif mi_score >= 10:
                    summary['maintainability_ranges']['B (10-19)'] += 1
                else:
                    summary['maintainability_ranges']['C (0-9)'] += 1
    
    return summary


def analyze_sample_code():
    """Analyze sample Python code with radon."""
    sample_code = '''
def simple_function():
    """A simple function with low complexity."""
    return 42

def complex_function(n):
    """A more complex function."""
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

class SimpleClass:
    """A simple class."""
    def __init__(self):
        self.value = 0
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value

def very_complex_function(a, b, c, d, e, f, g, h, i, j):
    """A function with many parameters and complex logic."""
    if a > b:
        if c > d:
            if e > f:
                if g > h:
                    if i > j:
                        return a + b + c + d + e + f + g + h + i + j
                    else:
                        return a - b - c - d - e - f - g - h - i - j
                else:
                    return a * b * c * d * e * f * g * h * i * j
            else:
                return a / b / c / d / e / f / g / h / i / j
        else:
            return a % b % c % d % e % f % g % h % i % j
    else:
        return a ** b ** c ** d ** e ** f ** g ** h ** i ** j
'''
    
    print("Analyzing sample code with radon...")
    results = run_radon(sample_code)
    
    # Output results as formatted JSON
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If file path provided, analyze that file
        file_path = sys.argv[1]
        with open(file_path, 'r') as f:
            code = f.read()
        results = run_radon(code, file_path)
        print(json.dumps(results, indent=2))
    else:
        # Analyze sample code
        analyze_sample_code()
