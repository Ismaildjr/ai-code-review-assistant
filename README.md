# Static Code Analysis API

A FastAPI-based REST API that provides comprehensive Python code analysis using multiple static analysis tools, now with **AI-powered code review** capabilities.

## 🚀 Features

- **Multiple Analysis Tools**: pylint, flake8, radon, and bandit
- **AI-Powered Code Review**: LLM-generated code review reports
- **REST API**: Easy-to-use HTTP endpoints
- **Flexible Analysis**: Choose which tools to run
- **Structured Output**: JSON responses with detailed results
- **Comprehensive Metrics**: Summary statistics and categorized issues
- **Error Handling**: Graceful handling of failures and timeouts
- **Logging**: Structured logging for monitoring and debugging
- **Unit Tests**: Comprehensive test coverage with pytest
- **Multiple LLM Providers**: Support for Hugging Face and OpenAI

## 🛠️ Tools Included

- **pylint** - Code quality analysis and style checking
- **flake8** - Style guide enforcement and error checking  
- **radon** - Code complexity and maintainability metrics
- **bandit** - Security vulnerability scanning
- **AI Review** - LLM-powered code review and suggestions

## 📦 Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure the analysis tools are available in your PATH:
   - pylint
   - flake8
   - radon
   - bandit

## 🚀 Quick Start

### Start the API Server

```bash
python api.py
```

The server will start on `http://localhost:8000`

### Test the API

```bash
python test_client.py
```

### Run Unit Tests

```bash
pytest test_api.py -v
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "1.0.0",
  "tools_available": {
    "pylint": true,
    "flake8": true,
    "radon": true,
    "bandit": true
  }
}
```

#### 2. Get Available Tools
```http
GET /tools
```

**Response:**
```json
{
  "tools": {
    "pylint": {
      "name": "Pylint",
      "description": "Code quality analysis and style checking",
      "status": "available",
      "capabilities": ["code quality", "style checking", "error detection"]
    },
    "flake8": {
      "name": "Flake8",
      "description": "Style guide enforcement and error checking",
      "status": "available",
      "capabilities": ["style checking", "error detection", "import validation"]
    },
    "radon": {
      "name": "Radon",
      "description": "Code complexity and maintainability metrics",
      "status": "available",
      "capabilities": ["cyclomatic complexity", "maintainability index", "halstead metrics"]
    },
    "bandit": {
      "name": "Bandit",
      "description": "Security vulnerability scanning",
      "status": "available",
      "capabilities": ["security scanning", "vulnerability detection", "CWE mapping"]
    }
  }
}
```

#### 3. Analyze Code
```http
POST /analyze
```

**Request Body:**
```json
{
  "code": "def hello(): print('Hello World')",
  "filename": "example.py",
  "include_tools": ["pylint", "flake8", "radon", "bandit"]
}
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2024-01-01T12:00:00",
  "execution_time_ms": 1250.5,
  "filename": "example.py",
  "results": {
    "pylint": { /* pylint results */ },
    "flake8": { /* flake8 results */ },
    "radon": { /* radon results */ },
    "bandit": { /* bandit results */ }
  },
  "summary": {
    "total_issues": 5,
    "total_functions": 3,
    "total_classes": 1,
    "security_issues": 2,
    "style_issues": 2,
    "quality_issues": 1,
    "complexity_issues": 1,
    "tools_executed": 4,
    "tools_failed": 0
  },
  "errors": []
}
```

#### 4. Analyze Plain Code
```http
POST /analyze/plain
```

**Request Body:** Plain Python code as text
**Headers:** `Content-Type: text/plain`
**Query Parameters:**
- `filename` (optional): Filename for the code
- `include_tools` (optional): Comma-separated list of tools (default: all)

#### 5. AI-Powered Code Review
```http
POST /review
```

**Request Body:**
```json
{
  "code": "def hello(): print('Hello World')",
  "filename": "example.py",
  "include_tools": ["pylint", "flake8", "radon", "bandit"]
}
```

**Response:** Same as `/analyze` but includes `ai_review` section with LLM-generated review.

#### 6. AI Review with Plain Code
```http
POST /review/plain
```

**Request Body:** Plain Python code as text
**Headers:** `Content-Type: text/plain`
**Query Parameters:**
- `filename` (optional): Filename for the code
- `include_tools` (optional): Comma-separated list of tools
- `llm_provider` (optional): LLM provider ("huggingface" or "openai")

**AI Review Response Example:**
```json
{
  "success": true,
  "results": {
    "pylint": { /* pylint results */ },
    "flake8": { /* flake8 results */ },
    "radon": { /* radon results */ },
    "bandit": { /* bandit results */ },
    "ai_review": {
      "success": true,
      "review": "🤖 AI-generated code review with:\n- Bug identification\n- Style suggestions\n- Security recommendations\n- Improvement tips",
      "execution_time_ms": 2500.0,
      "provider": "huggingface"
    }
  }
}
```

#### 7. Professional HTML Report Generation
```http
POST /report/html
```

**Request Body:** Plain Python code as text
**Headers:** `Content-Type: text/plain`
**Query Parameters:**
- `filename` (optional): Filename for the code
- `include_tools` (optional): Comma-separated list of tools
- `llm_provider` (optional): LLM provider ("huggingface" or "openai")
- `company_name` (optional): Company name for report branding
- `logo_url` (optional): URL to company logo

**Response:** Professional HTML report file for download

**HTML Report Features:**
- 🎨 **Modern Design**: Beautiful, responsive UI with professional styling
- 📊 **Executive Summary**: Key metrics and risk assessment
- 🔍 **Detailed Analysis**: Tool-by-tool breakdown with issue details
- 🤖 **AI Review Section**: Highlighted AI-generated insights
- 💡 **Recommendations**: Actionable next steps and best practices
- 🖨️ **Print-Ready**: Optimized for printing and PDF generation
- 🏢 **Branded**: Customizable company name and logo
- 📱 **Responsive**: Works perfectly on all devices

## 🔧 Usage Examples

### Python Client

```python
import requests

# Analyze code
response = requests.post("http://localhost:8000/analyze", json={
    "code": "def test(): pass",
    "include_tools": ["bandit", "radon"]
})

if response.status_code == 200:
    results = response.json()
    print(f"Found {results['summary']['total_issues']} issues")
```

### cURL

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello(): print(\"Hello\")",
    "filename": "test.py"
  }'
```

### JavaScript/Node.js

```javascript
const response = await fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    code: 'def hello(): print("Hello")',
    filename: 'test.py'
  })
});

const results = await response.json();
console.log(`Found ${results.summary.total_issues} issues`);
```

## 🧪 Testing

### Run All Tests
```bash
pytest test_api.py -v
```

### Run Specific Test Classes
```bash
pytest test_api.py::TestHealthEndpoints -v
pytest test_api.py::TestAnalysisEndpoint -v
```

### Run with Coverage
```bash
pytest test_api.py --cov=api --cov-report=html
```

## 📁 Project Structure

```
ai-code-review-assistant/
├── api.py                 # FastAPI application
├── config.py              # Configuration settings
├── test_api.py            # Unit tests
├── test_client.py         # Test client script
├── test_ai_review.py      # AI review test script
├── test_html_report.py    # HTML report test script
├── llm_reviewer.py        # LLM integration module
├── html_report_generator.py # Professional HTML report generator
├── pylint_analyzer.py     # Pylint wrapper
├── flake8_analyzer.py     # Flake8 wrapper
├── radon_analyzer.py      # Radon wrapper
├── bandit_analyzer.py     # Bandit wrapper
├── run_all_analyzers.py   # CLI script
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## ⚙️ Configuration

The API can be configured using environment variables:

```bash
# API Configuration
export API_HOST=0.0.0.0
export API_PORT=8000

# Performance
export MAX_CODE_SIZE=1000000
export REQUEST_TIMEOUT=120

# Logging
export LOG_LEVEL=INFO
export LOG_FILE=/var/log/api.log

# Development
export DEBUG=true
export RELOAD=true

# LLM Configuration (for AI Review)
export HF_TOKEN=your_huggingface_token_here
export OPENAI_API_KEY=your_openai_api_key_here
```

## 🤖 AI Code Review Setup

The AI-powered code review requires API keys for LLM services:

### Hugging Face (Recommended)
1. Get your token from [Hugging Face](https://huggingface.co/settings/tokens)
2. Set environment variable: `export HF_TOKEN=your_token_here`

### OpenAI
1. Get your API key from [OpenAI](https://platform.openai.com/api-keys)
2. Set environment variable: `export OPENAI_API_KEY=your_key_here`

### Testing AI Review
```bash
# Test the AI review functionality
python test_ai_review.py
```

## 🔍 Monitoring and Logging

The API includes structured logging for monitoring:

- **Request logging**: All API requests are logged with timing information
- **Tool execution**: Individual tool execution results are logged
- **Error logging**: Detailed error information for debugging
- **Performance metrics**: Execution time tracking for optimization

## 🚀 Deployment

### Development
```bash
python api.py
```

### Production with uvicorn
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (example)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include code examples and error messages
