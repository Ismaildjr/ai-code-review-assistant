#!/usr/bin/env python3
"""
Professional HTML Report Generator for AI Code Review
Creates beautiful, client-ready reports with modern UI/UX design.
"""

import os
import json
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

class HTMLReportGenerator:
    """Generates professional HTML reports for code review results."""
    
    def __init__(self, company_name: str = "CodeReview Pro", logo_url: str = None):
        """
        Initialize the HTML report generator.
        
        Args:
            company_name: Company name for branding
            logo_url: URL to company logo (optional)
        """
        self.company_name = company_name
        self.logo_url = logo_url
        self.report_id = str(uuid.uuid4())[:8]
        
    def generate_report(self, analysis_results: Dict[str, Any], 
                       code: str, filename: str = None) -> str:
        """
        Generate a complete HTML report.
        
        Args:
            analysis_results: Results from the API
            code: The analyzed code
            filename: Optional filename
            
        Returns:
            Complete HTML report as string
        """
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Review Report - {filename or 'Python Code'}</title>
    <style>
        {self._get_css_styles()}
    </style>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    {self._generate_header(timestamp)}
    {self._generate_executive_summary(analysis_results)}
    {self._generate_code_section(code, filename)}
    {self._generate_detailed_analysis(analysis_results)}
    {self._generate_ai_review_section(analysis_results)}
    {self._generate_recommendations(analysis_results)}
    {self._generate_footer()}
    
    <script>
        {self._get_javascript()}
    </script>
</body>
</html>
        """
        
        return html_content
    
    def _get_css_styles(self) -> str:
        """Get the CSS styles for the report."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8fafc;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* Header Styles */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
        }
        
        .header-content {
            position: relative;
            z-index: 1;
        }
        
        .company-logo {
            width: 80px;
            height: 80px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }
        
        .company-logo i {
            font-size: 40px;
            color: white;
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 300;
        }
        
        .report-meta {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: -20px 20px 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #666;
        }
        
        .meta-item i {
            color: #667eea;
        }
        
        /* Executive Summary */
        .executive-summary {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
        }
        
        .summary-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .summary-header i {
            font-size: 2rem;
            color: #667eea;
        }
        
        .summary-header h2 {
            font-size: 1.8rem;
            color: #2d3748;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }
        
        .metric-card {
            background: #f8fafc;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e2e8f0;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .metric-label {
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .severity-indicator {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .severity-critical { background: #fed7d7; color: #c53030; }
        .severity-high { background: #feb2b2; color: #c05621; }
        .severity-medium { background: #fef5e7; color: #d69e2e; }
        .severity-low { background: #f0fff4; color: #38a169; }
        
        /* Code Section */
        .code-section {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        .code-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .code-header h3 {
            font-size: 1.5rem;
            color: #2d3748;
        }
        
        .copy-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background 0.2s;
        }
        
        .copy-btn:hover {
            background: #5a67d8;
        }
        
        .code-block {
            background: #1a202c;
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            position: relative;
        }
        
        .code-block pre {
            color: #e2e8f0;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
            margin: 0;
        }
        
        /* Analysis Results */
        .analysis-section {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        .section-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f1f5f9;
        }
        
        .section-header i {
            font-size: 1.5rem;
            color: #667eea;
        }
        
        .section-header h3 {
            font-size: 1.5rem;
            color: #2d3748;
        }
        
        .tool-results {
            display: grid;
            gap: 20px;
        }
        
        .tool-card {
            background: #f8fafc;
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }
        
        .tool-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .tool-name {
            font-weight: 600;
            color: #2d3748;
            font-size: 1.1rem;
        }
        
        .tool-status {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .status-success { background: #f0fff4; color: #38a169; }
        .status-error { background: #fed7d7; color: #c53030; }
        
        .issue-list {
            list-style: none;
        }
        
        .issue-item {
            background: white;
            padding: 12px 16px;
            margin-bottom: 8px;
            border-radius: 6px;
            border-left: 3px solid #e2e8f0;
            transition: border-color 0.2s;
        }
        
        .issue-item:hover {
            border-left-color: #667eea;
        }
        
        .issue-severity {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        /* AI Review Section */
        .ai-review-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 30px;
            color: white;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .ai-review-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="ai-pattern" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="0.8" fill="white" opacity="0.08"/><circle cx="25" cy="25" r="0.5" fill="white" opacity="0.05"/><circle cx="75" cy="75" r="0.6" fill="white" opacity="0.06"/></pattern></defs><rect width="100" height="100" fill="url(%23ai-pattern)"/></svg>');
            opacity: 0.4;
        }
        
        .ai-content {
            position: relative;
            z-index: 1;
        }
        
        .ai-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        .ai-header i {
            font-size: 2.5rem;
            color: white;
            background: rgba(255, 255, 255, 0.2);
            padding: 15px;
            border-radius: 50%;
            backdrop-filter: blur(10px);
        }
        
        .ai-header h3 {
            font-size: 2rem;
            color: white;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .ai-review-content {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            padding: 30px;
            border-radius: 12px;
            line-height: 1.8;
            font-size: 1.1rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .ai-review-content h2, .ai-review-content h3, .ai-review-content h4 {
            color: white;
            margin: 25px 0 15px 0;
            font-weight: 600;
        }
        
        .ai-review-content p {
            margin: 15px 0;
            color: rgba(255, 255, 255, 0.95);
        }
        
        .ai-review-content strong {
            color: white;
            font-weight: 700;
        }
        
        .ai-review-content code {
            background: rgba(0, 0, 0, 0.3);
            color: #fbbf24;
            padding: 4px 8px;
            border-radius: 6px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .ai-review-content pre {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            overflow-x: auto;
        }
        
        .ai-review-content ul {
            margin: 20px 0;
            padding-left: 25px;
        }
        
        .ai-review-content li {
            margin: 10px 0;
            color: rgba(255, 255, 255, 0.9);
        }
        
        .ai-review-content hr {
            border: none;
            border-top: 2px solid rgba(255, 255, 255, 0.3);
            margin: 30px 0;
        }
        
        .ai-review-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .ai-footer-item {
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(255, 255, 255, 0.1);
            padding: 12px 20px;
            border-radius: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }
        
        .ai-footer-item:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .ai-footer-item i {
            color: #fbbf24;
            font-size: 1.1rem;
        }
        
        .ai-footer-item span {
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        /* Recommendations */
        .recommendations-section {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        .recommendation-grid {
            display: grid;
            gap: 20px;
        }
        
        .recommendation-card {
            background: #f8fafc;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #48bb78;
        }
        
        .recommendation-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .recommendation-header i {
            color: #48bb78;
            font-size: 1.2rem;
        }
        
        .recommendation-title {
            font-weight: 600;
            color: #2d3748;
        }
        
        .recommendation-card p {
            color: #4a5568;
            margin: 0;
            line-height: 1.6;
        }
        
        /* Footer */
        .footer {
            background: #2d3748;
            color: white;
            text-align: center;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .footer-left {
            text-align: left;
        }
        
        .footer-right {
            text-align: right;
        }
        
        .footer h4 {
            margin-bottom: 10px;
            color: #667eea;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 0 15px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .report-meta {
                flex-direction: column;
                text-align: center;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            
            .footer-content {
                flex-direction: column;
                text-align: center;
            }
            
            .ai-review-section {
                padding: 25px;
                margin: 0 15px 30px;
            }
            
            .ai-header {
                flex-direction: column;
                text-align: center;
                gap: 15px;
            }
            
            .ai-header h3 {
                font-size: 1.6rem;
            }
            
            .ai-review-content {
                padding: 20px;
            }
            
            .ai-review-footer {
                flex-direction: column;
                gap: 15px;
            }
            
            .ai-footer-item {
                width: 100%;
                justify-content: center;
            }
        }
        
        /* Print Styles */
        @media print {
            body {
                background: white;
            }
            
            .header, .footer {
                -webkit-print-color-adjust: exact;
                color-adjust: exact;
            }
            
            .code-block {
                background: #f8f9fa !important;
                color: #333 !important;
            }
        }
        """
    
    def _generate_header(self, timestamp: str) -> str:
        """Generate the report header."""
        logo_html = ""
        if self.logo_url:
            logo_html = f'<img src="{self.logo_url}" alt="Logo" class="company-logo">'
        else:
            logo_html = '<div class="company-logo"><i class="fas fa-code"></i></div>'
        
        return f"""
        <div class="header">
            <div class="header-content">
                {logo_html}
                <h1>Code Review Report</h1>
                <p>Professional analysis and AI-powered insights</p>
            </div>
        </div>
        
        <div class="container">
            <div class="report-meta">
                <div class="meta-item">
                    <i class="fas fa-calendar"></i>
                    <span>Generated: {timestamp}</span>
                </div>
                <div class="meta-item">
                    <i class="fas fa-fingerprint"></i>
                    <span>Report ID: {self.report_id}</span>
                </div>
                <div class="meta-item">
                    <i class="fas fa-building"></i>
                    <span>{self.company_name}</span>
                </div>
            </div>
        </div>
        """
    
    def _generate_executive_summary(self, results: Dict[str, Any]) -> str:
        """Generate the executive summary section."""
        summary = results.get('summary', {})
        
        total_issues = summary.get('total_issues', 0)
        security_issues = summary.get('security_issues', 0)
        style_issues = summary.get('style_issues', 0)
        quality_issues = summary.get('quality_issues', 0)
        complexity_issues = summary.get('complexity_issues', 0)
        tools_executed = summary.get('tools_executed', 0)
        
        # Determine overall severity
        if security_issues > 0:
            overall_severity = "critical" if security_issues > 2 else "high"
        elif total_issues > 10:
            overall_severity = "medium"
        else:
            overall_severity = "low"
        
        severity_class = f"severity-{overall_severity}"
        severity_text = overall_severity.upper()
        
        return f"""
        <div class="container">
            <div class="executive-summary">
                <div class="summary-header">
                    <i class="fas fa-chart-line"></i>
                    <h2>Executive Summary</h2>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{total_issues}</div>
                        <div class="metric-label">Total Issues</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{security_issues}</div>
                        <div class="metric-label">Security Issues</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{style_issues}</div>
                        <div class="metric-label">Style Issues</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{complexity_issues}</div>
                        <div class="metric-label">Complexity Issues</div>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <span class="severity-indicator {severity_class}">
                        Overall Risk Level: {severity_text}
                    </span>
                </div>
            </div>
        </div>
        """
    
    def _generate_code_section(self, code: str, filename: str) -> str:
        """Generate the code display section."""
        display_name = filename or "Python Code"
        
        return f"""
        <div class="container">
            <div class="code-section">
                <div class="code-header">
                    <h3><i class="fas fa-code"></i> Analyzed Code</h3>
                    <button class="copy-btn" onclick="copyCode()">
                        <i class="fas fa-copy"></i> Copy Code
                    </button>
                </div>
                <div class="code-block">
                    <pre><code id="code-content">{self._escape_html(code)}</code></pre>
                </div>
                <div style="margin-top: 15px; color: #666; font-size: 0.9rem;">
                    <i class="fas fa-file-code"></i> File: {display_name}
                </div>
            </div>
        </div>
        """
    
    def _generate_detailed_analysis(self, results: Dict[str, Any]) -> str:
        """Generate the detailed analysis section."""
        analysis_html = ""
        
        # Only process actual analysis tools
        analysis_tools = ['pylint', 'flake8', 'radon', 'bandit']
        
        for tool_name, tool_results in results.items():
            # Skip non-analysis tools and ai_review
            if tool_name not in analysis_tools or tool_name == "ai_review":
                continue
                
            if not isinstance(tool_results, dict):
                continue
                
            tool_display_name = tool_name.upper()
            tool_icon = self._get_tool_icon(tool_name)
            
            if tool_results.get('success'):
                status_class = "status-success"
                status_text = "SUCCESS"
                
                # Generate issues list
                issues_html = self._generate_issues_list(tool_name, tool_results)
                
                analysis_html += f"""
                <div class="tool-card">
                    <div class="tool-header">
                        <div class="tool-name">
                            <i class="{tool_icon}"></i> {tool_display_name}
                        </div>
                        <span class="tool-status {status_class}">{status_text}</span>
                    </div>
                    {issues_html}
                </div>
                """
            else:
                status_class = "status-error"
                status_text = "ERROR"
                error_msg = tool_results.get('error', 'Unknown error')
                
                analysis_html += f"""
                <div class="tool-card">
                    <div class="tool-header">
                        <div class="tool-name">
                            <i class="{tool_icon}"></i> {tool_display_name}
                        </div>
                        <span class="tool-status {status_class}">{status_text}</span>
                    </div>
                    <div style="color: #c53030; padding: 10px; background: #fed7d7; border-radius: 4px;">
                        <i class="fas fa-exclamation-triangle"></i> {error_msg}
                    </div>
                </div>
                """
        
        return f"""
        <div class="container">
            <div class="analysis-section">
                <div class="section-header">
                    <i class="fas fa-microscope"></i>
                    <h3>Detailed Analysis Results</h3>
                </div>
                <div class="tool-results">
                    {analysis_html}
                </div>
            </div>
        </div>
        """
    
    def _generate_issues_list(self, tool_name: str, tool_results: Dict[str, Any]) -> str:
        """Generate the issues list for a specific tool."""
        if tool_name == "pylint" and 'issues' in tool_results:
            issues = tool_results['issues']
            if not issues:
                return '<div style="color: #38a169; padding: 10px;"><i class="fas fa-check-circle"></i> No issues found</div>'
            
            issues_html = '<ul class="issue-list">'
            for issue in issues[:10]:  # Limit to first 10 issues
                message = issue.get('message', 'Unknown issue')
                issues_html += f'<li class="issue-item">{message}</li>'
            issues_html += '</ul>'
            return issues_html
            
        elif tool_name == "flake8" and 'issues' in tool_results:
            issues = tool_results['issues']
            if not issues:
                return '<div style="color: #38a169; padding: 10px;"><i class="fas fa-check-circle"></i> No issues found</div>'
            
            issues_html = '<ul class="issue-list">'
            for issue in issues[:10]:
                message = issue.get('message', 'Unknown issue')
                issues_html += f'<li class="issue-item">{message}</li>'
            issues_html += '</ul>'
            return issues_html
            
        elif tool_name == "bandit" and 'results' in tool_results:
            results = tool_results['results']
            if 'results' in results:
                bandit_issues = results['results']
                if not bandit_issues:
                    return '<div style="color: #38a169; padding: 10px;"><i class="fas fa-check-circle"></i> No security issues found</div>'
                
                issues_html = '<ul class="issue-list">'
                for issue in bandit_issues[:10]:
                    severity = issue.get('issue_severity', 'UNKNOWN')
                    message = issue.get('issue_text', 'Unknown security issue')
                    severity_class = f"severity-{severity.lower()}"
                    issues_html += f'''
                    <li class="issue-item">
                        <span class="issue-severity {severity_class}">{severity}</span>
                        <div>{message}</div>
                    </li>
                    '''
                issues_html += '</ul>'
                return issues_html
        
        # Default case - show summary
        summary = tool_results.get('summary', {})
        if summary:
            summary_items = []
            for key, value in summary.items():
                if isinstance(value, (int, float)) and value > 0:
                    summary_items.append(f"{key.replace('_', ' ').title()}: {value}")
            
            if summary_items:
                return '<div style="padding: 10px; background: #f1f5f9; border-radius: 4px;">' + \
                       '<br>'.join(summary_items) + '</div>'
        
        return '<div style="color: #666; padding: 10px;"><i class="fas fa-info-circle"></i> Analysis completed</div>'
    
    def _generate_ai_review_section(self, results: Dict[str, Any]) -> str:
        """Generate the AI review section."""
        ai_review = results.get('ai_review', {})
        
        if not ai_review or not ai_review.get('success'):
            return f"""
            <div class="container">
                <div class="ai-review-section">
                    <div class="ai-content">
                        <div class="ai-header">
                            <i class="fas fa-robot"></i>
                            <h3>AI Code Review</h3>
                        </div>
                        <div class="ai-review-content">
                            <i class="fas fa-exclamation-triangle"></i> 
                            AI review could not be generated. {ai_review.get('error', 'Unknown error')}
                        </div>
                    </div>
                </div>
            </div>
            """
        
        review_text = ai_review.get('review', 'No review content available')
        provider = ai_review.get('provider', 'Unknown')
        execution_time = ai_review.get('execution_time_ms', 0)
        
        # Convert the AI review text to proper HTML
        formatted_review = self._format_ai_review_text(review_text)
        
        return f"""
        <div class="container">
            <div class="ai-review-section">
                <div class="ai-content">
                    <div class="ai-header">
                        <i class="fas fa-robot"></i>
                        <h3>AI-Powered Code Review</h3>
                    </div>
                    <div class="ai-review-content">
                        {formatted_review}
                    </div>
                    <div class="ai-review-footer">
                        <div class="ai-footer-item">
                            <i class="fas fa-brain"></i>
                            <span>Powered by {provider.upper()}</span>
                        </div>
                        <div class="ai-footer-item">
                            <i class="fas fa-clock"></i>
                            <span>Generated in {execution_time:.0f}ms</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> str:
        """Generate the recommendations section."""
        summary = results.get('summary', {})
        
        recommendations = []
        
        if summary.get('security_issues', 0) > 0:
            recommendations.append({
                'icon': 'fas fa-shield-alt',
                'title': 'Security Improvements',
                'description': 'Address security vulnerabilities identified by Bandit analysis'
            })
        
        if summary.get('style_issues', 0) > 0:
            recommendations.append({
                'icon': 'fas fa-paint-brush',
                'title': 'Code Style',
                'description': 'Follow PEP 8 style guidelines and fix formatting issues'
            })
        
        if summary.get('complexity_issues', 0) > 0:
            recommendations.append({
                'icon': 'fas fa-project-diagram',
                'title': 'Complexity Reduction',
                'description': 'Refactor complex functions to improve maintainability'
            })
        
        if not recommendations:
            recommendations.extend([
                {
                    'icon': 'fas fa-thumbs-up',
                    'title': 'Code Quality',
                    'description': 'Your code meets most quality standards. Keep up the good work!'
                },
                {
                    'icon': 'fas fa-rocket',
                    'title': 'Next Steps',
                    'description': 'Consider adding unit tests, documentation, and performance monitoring'
                },
                {
                    'icon': 'fas fa-users',
                    'title': 'Team Collaboration',
                    'description': 'Share this report with your team and establish code review processes'
                }
            ])
        
        recommendations_html = ""
        for rec in recommendations:
            recommendations_html += f"""
            <div class="recommendation-card">
                <div class="recommendation-header">
                    <i class="{rec['icon']}"></i>
                    <span class="recommendation-title">{rec['title']}</span>
                </div>
                <p>{rec['description']}</p>
            </div>
            """
        
        return f"""
        <div class="container">
            <div class="recommendations-section">
                <div class="section-header">
                    <i class="fas fa-lightbulb"></i>
                    <h3>Recommendations & Next Steps</h3>
                </div>
                <div class="recommendation-grid">
                    {recommendations_html}
                </div>
            </div>
        </div>
        """
    
    def _generate_footer(self) -> str:
        """Generate the report footer."""
        return f"""
        <div class="container">
            <div class="footer">
                <div class="footer-content">
                    <div class="footer-left">
                        <h4>Generated by {self.company_name}</h4>
                        <p>Professional code review and analysis services</p>
                    </div>
                    <div class="footer-right">
                        <h4>Report Information</h4>
                        <p>Report ID: {self.report_id}</p>
                        <p>Generated: {datetime.now().strftime("%B %d, %Y")}</p>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _get_tool_icon(self, tool_name: str) -> str:
        """Get the appropriate icon for a tool."""
        icons = {
            'pylint': 'fas fa-search',
            'flake8': 'fas fa-check-double',
            'radon': 'fas fa-chart-line',
            'bandit': 'fas fa-shield-alt'
        }
        return icons.get(tool_name, 'fas fa-tools')
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    def _format_ai_review_text(self, text: str) -> str:
        """Convert AI review text to properly formatted HTML."""
        if not text:
            return "No review content available"
        
        # Split text into lines
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('<br>')
                continue
            
            # Handle headers (lines starting with # or ===)
            if line.startswith('###'):
                # H3 header
                header_text = line.replace('###', '').strip()
                if header_text:
                    formatted_lines.append(f'<h4 style="margin: 20px 0 10px 0; color: white; font-size: 1.2rem;">{header_text}</h4>')
            elif line.startswith('##'):
                # H2 header
                header_text = line.replace('##', '').strip()
                if header_text:
                    formatted_lines.append(f'<h3 style="margin: 25px 0 15px 0; color: white; font-size: 1.4rem;">{header_text}</h3>')
            elif line.startswith('#'):
                # H1 header
                header_text = line.replace('#', '').strip()
                if header_text:
                    formatted_lines.append(f'<h2 style="margin: 30px 0 20px 0; color: white; font-size: 1.6rem;">{header_text}</h2>')
            elif line.startswith('===') or line.startswith('---'):
                # Separator lines
                formatted_lines.append('<hr style="border: none; border-top: 1px solid rgba(255,255,255,0.3); margin: 20px 0;">')
            elif line.startswith('**') and line.endswith('**'):
                # Bold text
                bold_text = line[2:-2].strip()
                if bold_text:
                    formatted_lines.append(f'<strong style="color: white; font-weight: 600;">{bold_text}</strong>')
            elif line.startswith('* ') or line.startswith('- '):
                # List items
                list_text = line[2:].strip()
                if list_text:
                    formatted_lines.append(f'<li style="margin: 5px 0; padding-left: 10px;">{list_text}</li>')
            elif line.startswith('```'):
                # Code block start/end
                if line == '```':
                    formatted_lines.append('<pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin: 15px 0; overflow-x: auto;"><code style="color: white; font-family: monospace;">')
                elif line.startswith('```python'):
                    formatted_lines.append('<pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin: 15px 0; overflow-x: auto;"><code style="color: white; font-family: monospace;">')
                else:
                    formatted_lines.append('</code></pre>')
            elif line.startswith('`') and line.endswith('`'):
                # Inline code
                code_text = line[1:-1].strip()
                if code_text:
                    formatted_lines.append(f'<code style="background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; font-family: monospace;">{code_text}</code>')
            elif line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. ') or line.startswith('4. ') or line.startswith('5. '):
                # Numbered list items
                list_text = line[3:].strip()
                if list_text:
                    formatted_lines.append(f'<li style="margin: 5px 0; padding-left: 10px;">{list_text}</li>')
            else:
                # Regular paragraph text
                if line:
                    formatted_lines.append(f'<p style="margin: 10px 0; line-height: 1.6;">{line}</p>')
        
        # Join all formatted lines
        html_content = '\n'.join(formatted_lines)
        
        # Wrap list items in proper list tags
        html_content = html_content.replace('<li', '<ul style="margin: 15px 0; padding-left: 20px;"><li')
        html_content = html_content.replace('</li>', '</li></ul>')
        
        # Clean up multiple list tags
        html_content = html_content.replace('</ul><ul', '')
        html_content = html_content.replace('<ul><ul', '<ul')
        html_content = html_content.replace('</ul></ul>', '</ul>')
        
        return html_content
    
    def _get_javascript(self) -> str:
        """Get the JavaScript for interactive features."""
        return """
        function copyCode() {
            const codeElement = document.getElementById('code-content');
            const textArea = document.createElement('textarea');
            textArea.value = codeElement.textContent;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            const btn = event.target.closest('.copy-btn');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            btn.style.background = '#48bb78';
            
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.style.background = '#667eea';
            }, 2000);
        }
        
        // Add smooth scrolling for better UX
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        
        // Add print functionality
        function printReport() {
            window.print();
        }
        """
    
    def save_report(self, analysis_results: Dict[str, Any], code: str, 
                   filename: str = None, output_path: str = None) -> str:
        """
        Generate and save the HTML report to a file.
        
        Args:
            analysis_results: Results from the API
            code: The analyzed code
            filename: Optional filename for the code
            output_path: Optional output file path
            
        Returns:
            Path to the saved HTML file
        """
        html_content = self.generate_report(analysis_results, code, filename)
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"code_review_report_{timestamp}.html"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path


def create_report_generator(company_name: str = "CodeReview Pro", 
                           logo_url: str = None) -> HTMLReportGenerator:
    """
    Factory function to create an HTML report generator.
    
    Args:
        company_name: Company name for branding
        logo_url: URL to company logo
        
    Returns:
        Configured HTMLReportGenerator instance
    """
    return HTMLReportGenerator(company_name, logo_url)


# Example usage
if __name__ == "__main__":
    # Test the report generator
    generator = create_report_generator("My Code Review Company")
    
    # Sample data
    sample_results = {
        "summary": {
            "total_issues": 8,
            "security_issues": 2,
            "style_issues": 4,
            "quality_issues": 2,
            "complexity_issues": 1,
            "tools_executed": 4
        },
        "pylint": {
            "success": True,
            "summary": {"total_issues": 3},
            "issues": [
                {"message": "Function name should be snake_case"},
                {"message": "Unused variable 'temp'"},
                {"message": "Missing docstring"}
            ]
        },
        "ai_review": {
            "success": True,
            "review": "This code has several areas for improvement...",
            "provider": "huggingface",
            "execution_time_ms": 2500
        }
    }
    
    sample_code = """
def calculateSum(a, b):
    temp = a + b
    return temp

def very_long_function(a,b,c,d,e,f,g,h,i,j):
    print("This is too long")
    return a+b+c+d+e+f+g+h+i+j
"""
    
    # Generate and save report
    output_file = generator.save_report(sample_results, sample_code, "test_code.py")
    print(f"Report generated: {output_file}")
