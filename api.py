#!/usr/bin/env python3
"""
FastAPI wrapper for static code analysis tools.
Provides REST API endpoints for analyzing Python code.
"""

from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import logging
import json
import time
from datetime import datetime
import os
import uuid

# Import our analysis tools
from analyzers.pylint_analyzer import run_pylint_analysis
from analyzers.flake8_analyzer import run_flake8
from analyzers.radon_analyzer import run_radon
from analyzers.bandit_analyzer import run_bandit
from llm_reviewer import create_reviewer
from html_report_generator import create_report_generator

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Static Code Analysis API",
    description="API for analyzing Python code using multiple static analysis tools",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    # Create static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Request/Response models
class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Python code to analyze", min_length=1)
    filename: Optional[str] = Field(None, description="Optional filename for the code")
    include_tools: Optional[list[str]] = Field(
        default=["pylint", "flake8", "radon", "bandit"],
        description="List of analysis tools to use"
    )

class CodeAnalysisResponse(BaseModel):
    success: bool
    timestamp: str
    execution_time_ms: float
    filename: Optional[str]
    results: Dict[str, Any]
    summary: Dict[str, Any]
    errors: list[str]

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    tools_available: Dict[str, bool]

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with API health information."""
    logger.info("Health check requested")
    
    # Check which tools are available
    tools_available = {
        "pylint": True,  # Basic mode always available
        "flake8": True,  # Basic mode always available
        "radon": True,   # Fully functional
        "bandit": True   # Fully functional
    }
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        tools_available=tools_available
    )

@app.get("/ui")
async def web_ui():
    """Serve the web UI."""
    try:
        return FileResponse("static/index.html")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Web UI not found. Please ensure static/index.html exists.")

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify API is working."""
    return {"message": "API is working!", "timestamp": datetime.utcnow().isoformat()}

@app.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze Python code using multiple static analysis tools.
    
    Args:
        request: CodeAnalysisRequest containing the code to analyze
        
    Returns:
        CodeAnalysisResponse with comprehensive analysis results
    """
    start_time = time.time()
    logger.info(f"Code analysis requested for code length: {len(request.code)}")
    
    try:
        # Validate requested tools
        valid_tools = ["pylint", "flake8", "radon", "bandit"]
        requested_tools = [tool.lower() for tool in request.include_tools]
        
        for tool in requested_tools:
            if tool not in valid_tools:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid tool '{tool}'. Valid tools: {valid_tools}"
                )
        
        # Run analysis tools
        results = {}
        errors = []
        
        if "pylint" in requested_tools:
            logger.info("Running pylint analysis")
            try:
                pylint_results = run_pylint_analysis(request.code, request.filename)
                results["pylint"] = pylint_results
                logger.info(f"Pylint completed: {pylint_results.get('summary', {}).get('total_issues', 0)} issues found")
            except Exception as e:
                error_msg = f"Pylint failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["pylint"] = {"error": error_msg}
        
        if "flake8" in requested_tools:
            logger.info("Running flake8 analysis")
            try:
                flake8_results = run_flake8(request.code, request.filename)
                results["flake8"] = flake8_results
                logger.info(f"Flake8 completed: {flake8_results.get('summary', {}).get('total_issues', 0)} issues found")
            except Exception as e:
                error_msg = f"Flake8 failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["flake8"] = {"error": error_msg}
        
        if "radon" in requested_tools:
            logger.info("Running radon analysis")
            try:
                radon_results = run_radon(request.code, request.filename)
                results["radon"] = radon_results
                logger.info(f"Radon completed: {radon_results.get('summary', {}).get('total_functions', 0)} functions analyzed")
            except Exception as e:
                error_msg = f"Radon failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["radon"] = {"error": error_msg}
        
        if "bandit" in requested_tools:
            logger.info("Running bandit analysis")
            try:
                bandit_results = run_bandit(request.code, request.filename)
                results["bandit"] = bandit_results
                logger.info(f"Bandit completed: {bandit_results.get('summary', {}).get('total_issues', 0)} security issues found")
            except Exception as e:
                error_msg = f"Bandit failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["bandit"] = {"error": error_msg}
        
        # Calculate overall summary
        summary = calculate_overall_summary(results)
        
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        logger.info(f"Analysis completed in {execution_time:.2f}ms")
        
        return CodeAnalysisResponse(
            success=True,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_ms=execution_time,
            filename=request.filename,
            results=results,
            summary=summary,
            errors=errors
        )
        
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        error_msg = f"Analysis failed: {str(e)}"
        logger.error(error_msg)
        
        return CodeAnalysisResponse(
            success=False,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_ms=execution_time,
            filename=request.filename,
            results={},
            summary={},
            errors=[error_msg]
        )

@app.post("/analyze/plain", response_model=CodeAnalysisResponse)
async def analyze_plain_code(
    code: str = Body(..., media_type="text/plain"),
    filename: Optional[str] = Query(None, description="Optional filename for the code"),
    include_tools: Optional[str] = Query("pylint,flake8,radon,bandit", description="Comma-separated list of analysis tools to use")
):
    """
    Analyze Python code using multiple static analysis tools.
    Accepts plain Python code directly in the request body.
    
    Args:
        code: Python code as plain text
        filename: Optional filename for the code
        include_tools: Comma-separated list of tools to use
        
    Returns:
        CodeAnalysisResponse with comprehensive analysis results
    """
    start_time = time.time()
    logger.info(f"Plain code analysis requested for code length: {len(code)}")
    
    try:
        # Parse include_tools from comma-separated string
        tools_list = [tool.strip().lower() for tool in include_tools.split(",")]
        
        # Validate requested tools
        valid_tools = ["pylint", "flake8", "radon", "bandit"]
        requested_tools = [tool for tool in tools_list if tool in valid_tools]
        
        if not requested_tools:
            raise HTTPException(
                status_code=400, 
                detail=f"No valid tools specified. Valid tools: {valid_tools}"
            )
        
        # Run analysis tools
        results = {}
        errors = []
        
        if "pylint" in requested_tools:
            logger.info("Running pylint analysis")
            try:
                pylint_results = run_pylint_analysis(code, filename)
                results["pylint"] = pylint_results
                logger.info(f"Pylint completed: {pylint_results.get('summary', {}).get('total_issues', 0)} issues found")
            except Exception as e:
                error_msg = f"Pylint failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["pylint"] = {"error": error_msg}
        
        if "flake8" in requested_tools:
            logger.info("Running flake8 analysis")
            try:
                flake8_results = run_flake8(code, filename)
                results["flake8"] = flake8_results
                logger.info(f"Flake8 completed: {flake8_results.get('summary', {}).get('total_issues', 0)} issues found")
            except Exception as e:
                error_msg = f"Flake8 failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["flake8"] = {"error": error_msg}
        
        if "radon" in requested_tools:
            logger.info("Running radon analysis")
            try:
                radon_results = run_radon(code, filename)
                results["radon"] = radon_results
                logger.info(f"Radon completed: {radon_results.get('summary', {}).get('total_functions', 0)} functions analyzed")
            except Exception as e:
                error_msg = f"Radon failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["radon"] = {"error": error_msg}
        
        if "bandit" in requested_tools:
            logger.info("Running bandit analysis")
            try:
                bandit_results = run_bandit(code, filename)
                results["bandit"] = bandit_results
                logger.info(f"Bandit completed: {bandit_results.get('summary', {}).get('total_issues', 0)} security issues found")
            except Exception as e:
                error_msg = f"Bandit failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["bandit"] = {"error": error_msg}
        
        # Calculate overall summary
        summary = calculate_overall_summary(results)
        
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        logger.info(f"Analysis completed in {execution_time:.2f}ms")
        
        return CodeAnalysisResponse(
            success=True,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_ms=execution_time,
            filename=filename,
            results=results,
            summary=summary,
            errors=errors
        )
        
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        error_msg = f"Analysis failed: {str(e)}"
        logger.error(error_msg)
        
        return CodeAnalysisResponse(
            success=False,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_ms=execution_time,
            filename=filename,
            results={},
            summary={},
            errors=[error_msg]
        )

@app.get("/tools")
async def get_available_tools():
    """Get information about available analysis tools."""
    logger.info("Available tools requested")
    
    tools_info = {
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
    
    return {"tools": tools_info}

@app.post("/review", response_model=CodeAnalysisResponse)
async def review_code_with_ai(request: CodeAnalysisRequest):
    """
    Analyze Python code and generate AI-powered code review.
    
    Args:
        request: CodeAnalysisRequest containing the code to analyze and review
        
    Returns:
        CodeAnalysisResponse with analysis results and AI review
    """
    start_time = time.time()
    logger.info(f"AI code review requested for code length: {len(request.code)}")
    
    try:
        # First run static analysis
        valid_tools = ["pylint", "flake8", "radon", "bandit"]
        requested_tools = [tool.lower() for tool in request.include_tools]
        
        for tool in requested_tools:
            if tool not in valid_tools:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid tool '{tool}'. Valid tools: {valid_tools}"
                )
        
        # Run analysis tools
        results = {}
        errors = []
        
        if "pylint" in requested_tools:
            logger.info("Running pylint analysis")
            try:
                pylint_results = run_pylint_analysis(request.code, request.filename)
                results["pylint"] = pylint_results
                logger.info(f"Pylint completed: {pylint_results.get('summary', {}).get('total_issues', 0)} issues found")
            except Exception as e:
                error_msg = f"Pylint failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["pylint"] = {"error": error_msg}
        
        if "flake8" in requested_tools:
            logger.info("Running flake8 analysis")
            try:
                flake8_results = run_flake8(request.code, request.filename)
                results["flake8"] = flake8_results
                logger.info(f"Flake8 completed: {flake8_results.get('summary', {}).get('total_issues', 0)} issues found")
            except Exception as e:
                error_msg = f"Flake8 failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["flake8"] = {"error": error_msg}
        
        if "radon" in requested_tools:
            logger.info("Running radon analysis")
            try:
                radon_results = run_radon(request.code, request.filename)
                results["radon"] = radon_results
                logger.info(f"Radon completed: {radon_results.get('summary', {}).get('total_functions', 0)} functions analyzed")
            except Exception as e:
                error_msg = f"Radon failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["radon"] = {"error": error_msg}
        
        if "bandit" in requested_tools:
            logger.info("Running bandit analysis")
            try:
                bandit_results = run_bandit(request.code, request.filename)
                results["bandit"] = bandit_results
                logger.info(f"Bandit completed: {bandit_results.get('summary', {}).get('total_issues', 0)} security issues found")
            except Exception as e:
                error_msg = f"Bandit failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["bandit"] = {"error": error_msg}
        
        # Generate AI review
        logger.info("Generating AI code review")
        try:
            reviewer = create_reviewer("huggingface")  # Default to Hugging Face
            ai_review = reviewer.review_code(request.code, results)
            results["ai_review"] = ai_review
            logger.info("AI review completed successfully")
        except Exception as e:
            error_msg = f"AI review failed: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
            results["ai_review"] = {"error": error_msg}
        
        # Calculate overall summary
        summary = calculate_overall_summary(results)
        
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        logger.info(f"AI review completed in {execution_time:.2f}ms")
        
        return CodeAnalysisResponse(
            success=True,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_ms=execution_time,
            filename=request.filename,
            results=results,
            summary=summary,
            errors=errors
        )
        
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        error_msg = f"AI review failed: {str(e)}"
        logger.error(error_msg)
        
        return CodeAnalysisResponse(
            success=False,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_ms=execution_time,
            filename=request.filename,
            results={},
            summary={},
            errors=[error_msg]
        )

@app.post("/review/plain", response_model=CodeAnalysisResponse)
async def review_plain_code_with_ai(
    code: str = Body(..., media_type="text/plain"),
    filename: Optional[str] = Query(None, description="Optional filename for the code"),
    include_tools: Optional[str] = Query("pylint,flake8,radon,bandit", description="Comma-separated list of analysis tools to use"),
    llm_provider: Optional[str] = Query("huggingface", description="LLM provider (huggingface or openai)")
):
    """
    Analyze plain Python code and generate AI-powered code review.
    Accepts plain Python code directly in the request body.
    
    Args:
        code: Python code as plain text
        filename: Optional filename for the code
        include_tools: Comma-separated list of tools to use
        llm_provider: LLM service provider to use
        
    Returns:
        CodeAnalysisResponse with analysis results and AI review
    """
    start_time = time.time()
    logger.info(f"Plain code AI review requested for code length: {len(code)}")
    
    try:
        # Parse include_tools from comma-separated string
        tools_list = [tool.strip().lower() for tool in include_tools.split(",")]
        
        # Validate requested tools
        valid_tools = ["pylint", "flake8", "radon", "bandit"]
        requested_tools = [tool for tool in tools_list if tool in valid_tools]
        
        if not requested_tools:
            raise HTTPException(
                status_code=400, 
                detail=f"No valid tools specified. Valid tools: {valid_tools}"
            )
        
        # Run analysis tools
        results = {}
        errors = []
        
        if "pylint" in requested_tools:
            logger.info("Running pylint analysis")
            try:
                pylint_results = run_pylint_analysis(code, filename)
                results["pylint"] = pylint_results
                logger.info(f"Pylint completed: {pylint_results.get('summary', {}).get('total_issues', 0)} issues found")
            except Exception as e:
                error_msg = f"Pylint failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["pylint"] = {"error": error_msg}
        
        if "flake8" in requested_tools:
            logger.info("Running flake8 analysis")
            try:
                flake8_results = run_flake8(code, filename)
                results["flake8"] = flake8_results
                logger.info(f"Flake8 completed: {flake8_results.get('summary', {}).get('total_issues', 0)} issues found")
            except Exception as e:
                error_msg = f"Flake8 failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["flake8"] = {"error": error_msg}
        
        if "radon" in requested_tools:
            logger.info("Running radon analysis")
            try:
                radon_results = run_radon(code, filename)
                results["radon"] = radon_results
                logger.info(f"Radon completed: {radon_results.get('summary', {}).get('total_functions', 0)} functions analyzed")
            except Exception as e:
                error_msg = f"Radon failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["radon"] = {"error": error_msg}
        
        if "bandit" in requested_tools:
            logger.info("Running bandit analysis")
            try:
                bandit_results = run_bandit(code, filename)
                results["bandit"] = bandit_results
                logger.info(f"Bandit completed: {bandit_results.get('summary', {}).get('total_issues', 0)} security issues found")
            except Exception as e:
                error_msg = f"Bandit failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["bandit"] = {"error": error_msg}
        
        # Generate AI review
        logger.info(f"Generating AI code review using {llm_provider}")
        try:
            reviewer = create_reviewer(llm_provider)
            ai_review = reviewer.review_code(code, results)
            results["ai_review"] = ai_review
            logger.info("AI review completed successfully")
        except Exception as e:
            error_msg = f"AI review failed: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
            results["ai_review"] = {"error": error_msg}
        
        # Calculate overall summary
        summary = calculate_overall_summary(results)
        
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        logger.info(f"Plain code AI review completed in {execution_time:.2f}ms")
        
        return CodeAnalysisResponse(
            success=True,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_ms=execution_time,
            filename=filename,
            results=results,
            summary=summary,
            errors=errors
        )
        
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        error_msg = f"Plain code AI review failed: {str(e)}"
        logger.error(error_msg)
        
        return CodeAnalysisResponse(
            success=False,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_ms=execution_time,
            filename=filename,
            results={},
            summary={},
            errors=[error_msg]
        )

@app.post("/report/html")
async def generate_html_report(
    code: str = Body(..., media_type="text/plain"),
    filename: Optional[str] = Query(None, description="Optional filename for the code"),
    include_tools: Optional[str] = Query("pylint,flake8,radon,bandit", description="Comma-separated list of analysis tools to use"),
    llm_provider: Optional[str] = Query("huggingface", description="LLM provider (huggingface or openai)"),
    company_name: Optional[str] = Query("CodeReview Pro", description="Company name for report branding"),
    logo_url: Optional[str] = Query(None, description="URL to company logo (optional)")
):
    """
    Generate a professional HTML report with static analysis and AI review.
    Accepts plain Python code and returns a beautiful, client-ready HTML report.
    
    Args:
        code: Python code as plain text
        filename: Optional filename for the code
        include_tools: Comma-separated list of tools to use
        llm_provider: LLM service provider to use
        company_name: Company name for report branding
        logo_url: URL to company logo
        
    Returns:
        HTML report file for download
    """
    start_time = time.time()
    logger.info(f"HTML report generation requested for code length: {len(code)}")
    
    try:
        # Parse include_tools from comma-separated string
        tools_list = [tool.strip().lower() for tool in include_tools.split(",")]
        
        # Validate requested tools
        valid_tools = ["pylint", "flake8", "radon", "bandit"]
        requested_tools = [tool for tool in tools_list if tool in valid_tools]
        
        if not requested_tools:
            raise HTTPException(
                status_code=400, 
                detail=f"No valid tools specified. Valid tools: {valid_tools}"
            )
        
        # Run analysis tools
        results = {}
        errors = []
        
        if "pylint" in requested_tools:
            logger.info("Running pylint analysis")
            try:
                pylint_results = run_pylint_analysis(code, filename)
                results["pylint"] = pylint_results
                logger.info(f"Pylint completed: {pylint_results.get('summary', {}).get('total_issues', 0)} issues found")
            except Exception as e:
                error_msg = f"Pylint failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["pylint"] = {"error": error_msg}
        
        if "flake8" in requested_tools:
            logger.info("Running flake8 analysis")
            try:
                flake8_results = run_flake8(code, filename)
                results["flake8"] = flake8_results
                logger.info(f"Flake8 completed: {flake8_results.get('summary', {}).get('total_issues', 0)} issues found")
            except Exception as e:
                error_msg = f"Flake8 failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["flake8"] = {"error": error_msg}
        
        if "radon" in requested_tools:
            logger.info("Running radon analysis")
            try:
                radon_results = run_radon(code, filename)
                results["radon"] = radon_results
                logger.info(f"Radon completed: {radon_results.get('summary', {}).get('total_functions', 0)} functions analyzed")
            except Exception as e:
                error_msg = f"Radon failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["radon"] = {"error": error_msg}
        
        if "bandit" in requested_tools:
            logger.info("Running bandit analysis")
            try:
                bandit_results = run_bandit(code, filename)
                results["bandit"] = bandit_results
                logger.info(f"Bandit completed: {bandit_results.get('summary', {}).get('total_issues', 0)} security issues found")
            except Exception as e:
                error_msg = f"Bandit failed: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results["bandit"] = {"error": error_msg}
        
        # Generate AI review
        logger.info(f"Generating AI code review using {llm_provider}")
        try:
            reviewer = create_reviewer(llm_provider)
            ai_review = reviewer.review_code(code, results)
            results["ai_review"] = ai_review
            logger.info("AI review completed successfully")
        except Exception as e:
            error_msg = f"AI review failed: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
            results["ai_review"] = {"error": error_msg}
        
        # Calculate overall summary
        summary = calculate_overall_summary(results)
        results["summary"] = summary
        
        # Generate HTML report
        logger.info("Generating professional HTML report")
        try:
            report_generator = create_report_generator(company_name, logo_url)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"code_review_report_{timestamp}.html"
            
            # Save report to temporary file
            report_path = report_generator.save_report(results, code, filename, report_filename)
            
            # Read the generated HTML file
            with open(report_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Clean up temporary file
            try:
                os.remove(report_path)
            except:
                pass
            
            execution_time = (time.time() - start_time) * 1000
            
            logger.info(f"HTML report generated successfully in {execution_time:.2f}ms")
            
            # Return HTML content with proper headers
            from fastapi.responses import HTMLResponse
            return HTMLResponse(
                content=html_content,
                headers={
                    "Content-Disposition": f"attachment; filename={report_filename}",
                    "X-Report-ID": str(uuid.uuid4())[:8],
                    "X-Execution-Time": f"{execution_time:.2f}ms"
                }
            )
            
        except Exception as e:
            error_msg = f"HTML report generation failed: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        error_msg = f"HTML report generation failed: {str(e)}"
        logger.error(error_msg)
        
        raise HTTPException(status_code=500, detail=error_msg)

def calculate_overall_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate overall summary statistics from all tool results."""
    summary = {
        "total_issues": 0,
        "total_functions": 0,
        "total_classes": 0,
        "security_issues": 0,
        "style_issues": 0,
        "quality_issues": 0,
        "complexity_issues": 0,
        "tools_executed": 0,
        "tools_failed": 0
    }
    
    # Count only actual analysis tools, exclude ai_review and other non-tools
    analysis_tools = ['pylint', 'flake8', 'radon', 'bandit']
    
    for tool_name, tool_results in results.items():
        # Skip non-analysis tools
        if tool_name not in analysis_tools:
            continue
            
        if isinstance(tool_results, dict) and tool_results.get('success'):
            summary['tools_executed'] += 1
            
            # Count issues
            if 'summary' in tool_results:
                tool_summary = tool_results['summary']
                
                if 'total_issues' in tool_summary:
                    summary['total_issues'] += tool_summary['total_issues']
                
                if 'total_functions' in tool_summary:
                    summary['total_functions'] += tool_summary['total_functions']
                
                if 'total_classes' in tool_summary:
                    summary['total_classes'] += tool_summary['total_classes']
                
                # Categorize issues by tool
                if tool_name == 'bandit':
                    summary['security_issues'] += tool_summary.get('total_issues', 0)
                elif tool_name in ['flake8', 'pylint']:
                    summary['style_issues'] += tool_summary.get('total_issues', 0)
                    summary['quality_issues'] += tool_summary.get('total_issues', 0)
                elif tool_name == 'radon':
                    # Count complex functions (complexity > 10)
                    if 'complexity_ranges' in tool_summary:
                        complexity_ranges = tool_summary['complexity_ranges']
                        summary['complexity_issues'] += (
                            complexity_ranges.get('C (11-20)', 0) +
                            complexity_ranges.get('D (21-50)', 0) +
                            complexity_ranges.get('E (51+)', 0)
                        )
        else:
            summary['tools_failed'] += 1
    
    return summary

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Static Code Analysis API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
