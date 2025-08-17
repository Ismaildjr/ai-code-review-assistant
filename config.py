#!/usr/bin/env python3
"""
Configuration file for the Static Code Analysis API.
"""

import os
from typing import List

# API Configuration
API_TITLE = "Static Code Analysis API"
API_DESCRIPTION = "API for analyzing Python code using multiple static analysis tools"
API_VERSION = "1.0.0"
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://localhost:8080",  # Vue dev server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "*"  # Allow all origins in development
]

# Available Analysis Tools
AVAILABLE_TOOLS = ["pylint", "flake8", "radon", "bandit"]

# Tool Configuration
TOOL_CONFIG = {
    "pylint": {
        "name": "Pylint",
        "description": "Code quality analysis and style checking",
        "status": "available",
        "capabilities": ["code quality", "style checking", "error detection"],
        "timeout": 30
    },
    "flake8": {
        "name": "Flake8",
        "description": "Style guide enforcement and error checking",
        "status": "available",
        "capabilities": ["style checking", "error detection", "import validation"],
        "timeout": 30
    },
    "radon": {
        "name": "Radon",
        "description": "Code complexity and maintainability metrics",
        "status": "available",
        "capabilities": ["cyclomatic complexity", "maintainability index", "halstead metrics"],
        "timeout": 30
    },
    "bandit": {
        "name": "Bandit",
        "description": "Security vulnerability scanning",
        "status": "available",
        "capabilities": ["security scanning", "vulnerability detection", "CWE mapping"],
        "timeout": 30
    }
}

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.getenv("LOG_FILE", None)  # Set to file path to log to file

# Performance Configuration
MAX_CODE_SIZE = int(os.getenv("MAX_CODE_SIZE", "1000000"))  # 1MB max
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "120"))  # 2 minutes

# Security Configuration
ENABLE_RATE_LIMITING = os.getenv("ENABLE_RATE_LIMITING", "false").lower() == "true"
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))

# Development Configuration
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
RELOAD = os.getenv("RELOAD", "false").lower() == "true"

# File Upload Configuration
ALLOWED_EXTENSIONS = [".py", ".pyw", ".pyx", ".pyi"]
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "1048576"))  # 1MB

# Cache Configuration
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "false").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes

# Health Check Configuration
HEALTH_CHECK_INTERVAL = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))  # 30 seconds

# Error Messages
ERROR_MESSAGES = {
    "code_too_large": "Code size exceeds maximum allowed limit",
    "invalid_tool": "Invalid analysis tool specified",
    "tool_unavailable": "Requested analysis tool is not available",
    "analysis_timeout": "Analysis timed out",
    "invalid_file_type": "Invalid file type. Only Python files are supported",
    "file_too_large": "File size exceeds maximum allowed limit",
    "rate_limit_exceeded": "Rate limit exceeded. Please try again later"
}

# Success Messages
SUCCESS_MESSAGES = {
    "analysis_completed": "Code analysis completed successfully",
    "health_check_passed": "API health check passed",
    "tools_available": "All analysis tools are available"
}
