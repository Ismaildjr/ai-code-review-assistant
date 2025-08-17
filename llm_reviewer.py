#!/usr/bin/env python3
"""
LLM-powered code reviewer that integrates with static analysis results.
Provides AI-generated code review reports based on analyzer findings.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMReviewer:
    """AI-powered code reviewer using LLM services."""
    
    def __init__(self, provider: str = "huggingface"):
        """
        Initialize the LLM reviewer.
        
        Args:
            provider: LLM service provider ("huggingface", "openai", or "local")
        """
        self.provider = provider
        self.setup_provider()
    
    def setup_provider(self):
        """Setup the LLM provider configuration."""
        if self.provider == "huggingface":
            self.api_url = "https://router.huggingface.co/v1/chat/completions"
            self.api_key = os.getenv("HF_TOKEN")
            if not self.api_key:
                logger.warning("HF_TOKEN not found in environment variables")
        elif self.provider == "openai":
            self.api_url = "https://api.openai.com/v1/chat/completions"
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                logger.warning("OPENAI_API_KEY not found in environment variables")
        else:
            logger.warning(f"Unsupported provider: {self.provider}")
    
    def generate_review_prompt(self, code: str, analysis_results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive prompt for the LLM based on analysis results.
        
        Args:
            code: The Python code to review
            analysis_results: Results from static analysis tools
            
        Returns:
            Formatted prompt string for the LLM
        """
        # Extract key findings from analysis results
        issues_summary = self._extract_issues_summary(analysis_results)
        
        prompt = f"""You are an AI code reviewer. Review the following Python code for:

1. Bugs and errors
2. Code style issues  
3. Security vulnerabilities
4. Suggestions for improvement

Here is the code to review:

```python
{code}
```

Static analysis tools found the following issues:

{issues_summary}

Please provide a comprehensive review that:
1. Explains each issue in simple, clear terms
2. Suggests specific improvements with code examples
3. Recommends best practices and coding standards
4. Prioritizes issues by severity (critical, high, medium, low)
5. Provides actionable next steps for the developer

Format your response in a clear, structured manner with sections for each category of issues.
"""
        return prompt
    
    def _extract_issues_summary(self, analysis_results: Dict[str, Any]) -> str:
        """
        Extract and format a summary of issues from analysis results.
        
        Args:
            analysis_results: Results from static analysis tools
            
        Returns:
            Formatted string summary of issues
        """
        summary_parts = []
        
        for tool_name, tool_results in analysis_results.items():
            if not isinstance(tool_results, dict) or not tool_results.get('success'):
                continue
                
            if tool_name == "pylint":
                pylint_summary = tool_results.get('summary', {})
                total_issues = pylint_summary.get('total_issues', 0)
                if total_issues > 0:
                    summary_parts.append(f"Pylint: {total_issues} code quality/style issues found")
                    
                    # Add specific issue details if available
                    if 'issues' in tool_results:
                        for issue in tool_results['issues'][:5]:  # Limit to first 5 issues
                            summary_parts.append(f"  - {issue.get('message', 'Unknown issue')}")
            
            elif tool_name == "flake8":
                flake8_summary = tool_results.get('summary', {})
                total_issues = flake8_summary.get('total_issues', 0)
                if total_issues > 0:
                    summary_parts.append(f"Flake8: {total_issues} style/error issues found")
                    
                    if 'issues' in tool_results:
                        for issue in tool_results['issues'][:5]:
                            summary_parts.append(f"  - {issue.get('message', 'Unknown issue')}")
            
            elif tool_name == "radon":
                radon_summary = tool_results.get('summary', {})
                total_functions = radon_summary.get('total_functions', 0)
                complexity_issues = radon_summary.get('complexity_issues', 0)
                
                if total_functions > 0:
                    summary_parts.append(f"Radon: {total_functions} functions analyzed")
                    if complexity_issues > 0:
                        summary_parts.append(f"  - {complexity_issues} functions have high complexity")
                    
                    # Add complexity ranges if available
                    if 'complexity_ranges' in radon_summary:
                        ranges = radon_summary['complexity_ranges']
                        for range_name, count in ranges.items():
                            if count > 0 and 'C' in range_name or 'D' in range_name or 'E' in range_name:
                                summary_parts.append(f"  - {count} functions in {range_name} complexity range")
            
            elif tool_name == "bandit":
                bandit_summary = tool_results.get('summary', {})
                total_issues = bandit_summary.get('total_issues', 0)
                high_severity = bandit_summary.get('high_severity', 0)
                
                if total_issues > 0:
                    summary_parts.append(f"Bandit: {total_issues} security issues found ({high_severity} high severity)")
                    
                    if 'results' in tool_results:
                        for issue in tool_results['results'].get('results', [])[:5]:
                            severity = issue.get('issue_severity', 'UNKNOWN')
                            message = issue.get('issue_text', 'Unknown security issue')
                            summary_parts.append(f"  - [{severity}] {message}")
        
        if not summary_parts:
            return "No issues found by static analysis tools."
        
        return "\n".join(summary_parts)
    
    def review_code(self, code: str, analysis_results: Dict[str, Any], 
                   max_tokens: int = 1000, temperature: float = 0.3) -> Dict[str, Any]:
        """
        Generate an AI-powered code review using the LLM.
        
        Args:
            code: The Python code to review
            analysis_results: Results from static analysis tools
            max_tokens: Maximum tokens for LLM response
            temperature: Creativity level (0.0 = focused, 1.0 = creative)
            
        Returns:
            Dictionary containing the review results
        """
        start_time = datetime.now()
        
        try:
            # Generate the review prompt
            prompt = self.generate_review_prompt(code, analysis_results)
            
            # Get LLM response
            llm_response = self._query_llm(prompt, max_tokens, temperature)
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                'success': True,
                'review': llm_response,
                'execution_time_ms': execution_time,
                'timestamp': datetime.utcnow().isoformat(),
                'provider': self.provider,
                'prompt_length': len(prompt),
                'response_length': len(llm_response)
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            error_msg = f"LLM review failed: {str(e)}"
            logger.error(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'execution_time_ms': execution_time,
                'timestamp': datetime.utcnow().isoformat(),
                'provider': self.provider
            }
    
    def _query_llm(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """
        Query the LLM service with the given prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            max_tokens: Maximum tokens for response
            temperature: Creativity level
            
        Returns:
            LLM response text
        """
        if not self.api_key:
            raise ValueError(f"API key not configured for {self.provider}")
        
        if self.provider == "huggingface":
            return self._query_huggingface(prompt, max_tokens, temperature)
        elif self.provider == "openai":
            return self._query_openai(prompt, max_tokens, temperature)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _query_huggingface(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Query Hugging Face API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "meta-llama/Llama-3.3-70B-Instruct:fireworks-ai",
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return str(result)
        else:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
    
    def _query_openai(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Query OpenAI API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return str(result)
        else:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")


def create_reviewer(provider: str = "huggingface") -> LLMReviewer:
    """
    Factory function to create an LLM reviewer instance.
    
    Args:
        provider: LLM service provider
        
    Returns:
        Configured LLMReviewer instance
    """
    return LLMReviewer(provider)


# Example usage
if __name__ == "__main__":
    # Test the LLM reviewer
    reviewer = create_reviewer("huggingface")
    
    sample_code = """
def calculate_sum(a, b):
    return a + b

def very_long_function(a,b,c,d,e,f,g,h,i,j):
    print("This is too long")
    return a+b+c+d+e+f+g+h+i+j
"""
    
    sample_analysis = {
        "pylint": {
            "success": True,
            "summary": {"total_issues": 2},
            "issues": [
                {"message": "Function name should be snake_case"},
                {"message": "Too many arguments"}
            ]
        },
        "radon": {
            "success": True,
            "summary": {"total_functions": 2, "complexity_issues": 1}
        }
    }
    
    print("=== Testing LLM Reviewer ===")
    result = reviewer.review_code(sample_code, sample_analysis)
    print(json.dumps(result, indent=2))
