// AI Code Review Assistant - Frontend Application
class CodeReviewApp {
    constructor() {
        // Auto-detect the current domain for production deployment
        this.apiBaseUrl = window.location.origin;
        this.analysisResults = null;
        this.initializeEventListeners();
    }
    
    initializeEventListeners() {
        // Add syntax highlighting to code input
        const codeInput = document.getElementById('codeInput');
        codeInput.addEventListener('input', () => {
            this.highlightSyntax(codeInput);
        });
        
        // Enable/disable buttons based on input
        codeInput.addEventListener('input', () => {
            this.updateButtonStates();
        });
        
        // Add filename change listener
        document.getElementById('filename').addEventListener('input', () => {
            this.updateButtonStates();
        });
    }
    
    updateButtonStates() {
        const codeInput = document.getElementById('codeInput');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const reportBtn = document.getElementById('reportBtn');
        
        const hasCode = codeInput.value.trim().length > 0;
        const hasResults = this.analysisResults !== null;
        
        analyzeBtn.disabled = !hasCode;
        reportBtn.disabled = !hasResults;
    }
    
    highlightSyntax(textarea) {
        // Simple syntax highlighting for Python
        const code = textarea.value;
        const highlighted = code
            .replace(/\b(def|class|import|from|as|if|else|elif|for|in|while|try|except|finally|with|return|True|False|None)\b/g, '<span style="color: #ff6b6b;">$1</span>')
            .replace(/\b(print|len|str|int|float|list|dict|set|tuple)\b/g, '<span style="color: #4ecdc4;">$1</span>')
            .replace(/\b(and|or|not|is|in)\b/g, '<span style="color: #45b7d1;">$1</span>')
            .replace(/(#.*)$/gm, '<span style="color: #95a5a6;">$1</span>')
            .replace(/(".*?"|'.*?')/g, '<span style="color: #f39c12;">$1</span>');
        
        // Note: This is a simple implementation. For production, use a proper syntax highlighter
    }
    
    async analyzeCode() {
        const code = document.getElementById('codeInput').value.trim();
        const filename = document.getElementById('filename').value.trim() || 'Python Code';
        
        if (!code) {
            this.showError('Please enter some code to analyze.');
            return;
        }
        
        // Get selected tools
        const selectedTools = this.getSelectedTools();
        if (selectedTools.length === 0) {
            this.showError('Please select at least one analysis tool.');
            return;
        }
        
        console.log('Starting analysis with:', { code: code.substring(0, 100) + '...', filename, selectedTools });
        
        // Update UI state
        this.setLoadingState(true);
        this.hideResults();
        
        try {
            // Build URL with query parameters
            const params = new URLSearchParams({
                filename: filename,
                include_tools: selectedTools.join(','),
                llm_provider: 'huggingface'
            });
            
            // Call the API
            const response = await fetch(`${this.apiBaseUrl}/review/plain?${params}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'text/plain',
                },
                body: code
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.analysisResults = await response.json();
            this.displayResults();
            this.showSuccess();
            this.updateButtonStates();
            
        } catch (error) {
            console.error('Analysis failed:', error);
            this.showError(`Analysis failed: ${error.message}`);
        } finally {
            this.setLoadingState(false);
        }
    }
    
    getSelectedTools() {
        const tools = [];
        if (document.getElementById('pylint').checked) tools.push('pylint');
        if (document.getElementById('flake8').checked) tools.push('flake8');
        if (document.getElementById('radon').checked) tools.push('radon');
        if (document.getElementById('bandit').checked) tools.push('bandit');
        return tools;
    }
    
    setLoadingState(loading) {
        const loadingDiv = document.getElementById('loading');
        const statusIndicator = document.getElementById('statusIndicator');
        const analyzeBtn = document.getElementById('analyzeBtn');
        
        if (loading) {
            loadingDiv.style.display = 'flex';
            statusIndicator.className = 'status-indicator status-loading';
            statusIndicator.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
            analyzeBtn.disabled = true;
        } else {
            loadingDiv.style.display = 'none';
            statusIndicator.className = 'status-indicator status-success';
            statusIndicator.innerHTML = '<i class="fas fa-check-circle"></i> Complete';
        }
    }
    
    displayResults() {
        if (!this.analysisResults) return;
        
        const resultsContent = document.getElementById('resultsContent');
        const downloadSection = document.getElementById('downloadSection');
        
        // Clear previous results
        resultsContent.innerHTML = '';
        
        // Display summary
        if (this.analysisResults.summary) {
            const summaryHtml = this.createSummaryHtml(this.analysisResults.summary);
            resultsContent.innerHTML += summaryHtml;
        }
        
        // Display tool results
        if (this.analysisResults.results) {
            Object.entries(this.analysisResults.results).forEach(([toolName, results]) => {
                if (toolName === 'ai_review') return; // Handle separately
                
                const toolHtml = this.createToolResultHtml(toolName, results);
                resultsContent.innerHTML += toolHtml;
            });
        }
        
        // Display AI review
        if (this.analysisResults.results?.ai_review) {
            const aiReviewHtml = this.createAIReviewHtml(this.analysisResults.results.ai_review);
            resultsContent.innerHTML += aiReviewHtml;
        }
        
        // Show results and download section
        resultsContent.classList.add('show');
        downloadSection.style.display = 'block';
    }
    
    createSummaryHtml(summary) {
        const totalIssues = summary.total_issues || 0;
        const securityIssues = summary.security_issues || 0;
        const styleIssues = summary.style_issues || 0;
        const complexityIssues = summary.complexity_issues || 0;
        
        let severityClass = 'status-success';
        let severityText = 'LOW';
        
        if (securityIssues > 0) {
            severityClass = securityIssues > 2 ? 'status-error' : 'status-loading';
            severityText = securityIssues > 2 ? 'CRITICAL' : 'HIGH';
        } else if (totalIssues > 10) {
            severityClass = 'status-loading';
            severityText = 'MEDIUM';
        }
        
        return `
            <div class="result-item">
                <div class="result-header">
                    <div class="result-title">
                        <i class="fas fa-chart-line"></i> Executive Summary
                    </div>
                    <span class="result-status ${severityClass}">${severityText}</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; margin-top: 15px;">
                    <div style="text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #667eea;">${totalIssues}</div>
                        <div style="font-size: 0.9rem; color: #666;">Total Issues</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #e74c3c;">${securityIssues}</div>
                        <div style="font-size: 0.9rem; color: #666;">Security Issues</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #f39c12;">${styleIssues}</div>
                        <div style="font-size: 0.9rem; color: #666;">Style Issues</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #9b59b6;">${complexityIssues}</div>
                        <div style="font-size: 0.9rem; color: #666;">Complexity Issues</div>
                    </div>
                </div>
            </div>
        `;
    }
    
    createToolResultHtml(toolName, results) {
        const toolDisplayNames = {
            'pylint': 'Pylint (Code Quality)',
            'flake8': 'Flake8 (Style)',
            'radon': 'Radon (Complexity)',
            'bandit': 'Bandit (Security)'
        };
        
        const toolIcons = {
            'pylint': 'fas fa-search',
            'flake8': 'fas fa-check-double',
            'radon': 'fas fa-chart-line',
            'bandit': 'fas fa-shield-alt'
        };
        
        const displayName = toolDisplayNames[toolName] || toolName;
        const icon = toolIcons[toolName] || 'fas fa-tools';
        
        if (results.success) {
            let content = '';
            
            if (results.summary) {
                const summaryItems = [];
                Object.entries(results.summary).forEach(([key, value]) => {
                    if (typeof value === 'number' && value > 0) {
                        summaryItems.push(`${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}: ${value}`);
                    }
                });
                
                if (summaryItems.length > 0) {
                    content = `<div style="padding: 10px; background: #f1f5f9; border-radius: 4px;">${summaryItems.join('<br>')}</div>`;
                }
            }
            
            if (results.issues && results.issues.length > 0) {
                content += '<ul style="margin-top: 10px; padding-left: 20px;">';
                results.issues.slice(0, 5).forEach(issue => {
                    content += `<li style="margin: 5px 0;">${issue.message || 'Unknown issue'}</li>`;
                });
                if (results.issues.length > 5) {
                    content += `<li style="color: #666; font-style: italic;">... and ${results.issues.length - 5} more issues</li>`;
                }
                content += '</ul>';
            }
            
            return `
                <div class="result-item">
                    <div class="result-header">
                        <div class="result-title">
                            <i class="${icon}"></i> ${displayName}
                        </div>
                        <span class="result-status status-success">SUCCESS</span>
                    </div>
                    ${content || '<div style="color: #38a169; padding: 10px;"><i class="fas fa-check-circle"></i> No issues found</div>'}
                </div>
            `;
        } else {
            return `
                <div class="result-item">
                    <div class="result-header">
                        <div class="result-title">
                            <i class="${icon}"></i> ${displayName}
                        </div>
                        <span class="result-status status-error">ERROR</span>
                    </div>
                    <div style="color: #c53030; padding: 10px; background: #fed7d7; border-radius: 4px;">
                        <i class="fas fa-exclamation-triangle"></i> ${results.error || 'Unknown error'}
                    </div>
                </div>
            `;
        }
    }
    
    createAIReviewHtml(aiReview) {
        if (!aiReview.success) {
            return `
                <div class="result-item">
                    <div class="result-header">
                        <div class="result-title">
                            <i class="fas fa-robot"></i> AI Code Review
                        </div>
                        <span class="result-status status-error">ERROR</span>
                    </div>
                    <div style="color: #c53030; padding: 10px; background: #fed7d7; border-radius: 4px;">
                        <i class="fas fa-exclamation-triangle"></i> AI review could not be generated: ${aiReview.error || 'Unknown error'}
                    </div>
                </div>
            `;
        }
        
        const reviewText = aiReview.review || 'No review content available';
        const provider = aiReview.provider || 'Unknown';
        const executionTime = aiReview.execution_time_ms || 0;
        
        return `
            <div class="result-item" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
                <div class="result-header">
                    <div class="result-title" style="color: white;">
                        <i class="fas fa-robot"></i> AI-Powered Code Review
                    </div>
                    <span class="result-status status-success">SUCCESS</span>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 15px; line-height: 1.6;">
                    ${this.formatReviewText(reviewText)}
                </div>
                <div style="margin-top: 15px; font-size: 0.9rem; opacity: 0.8;">
                    <i class="fas fa-brain"></i> Powered by ${provider.toUpperCase()} | 
                    <i class="fas fa-clock"></i> Generated in ${executionTime.toFixed(0)}ms
                </div>
            </div>
        `;
    }
    
    formatReviewText(text) {
        // Simple text formatting for display
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code style="background: rgba(0,0,0,0.3); padding: 2px 4px; border-radius: 3px;">$1</code>')
            .replace(/\n/g, '<br>');
    }
    
    async generateReport() {
        if (!this.analysisResults) {
            this.showError('Please analyze code first before generating a report.');
            return;
        }
        
        const code = document.getElementById('codeInput').value.trim();
        const filename = document.getElementById('filename').value.trim() || 'Python Code';
        const companyName = document.getElementById('companyName').value.trim() || 'CodeReview Pro';
        const logoUrl = document.getElementById('logoUrl').value.trim();
        
        try {
            // Build URL with query parameters
            const params = new URLSearchParams({
                filename: filename,
                include_tools: this.getSelectedTools().join(','),
                llm_provider: 'huggingface',
                company_name: companyName
            });
            
            if (logoUrl) {
                params.append('logo_url', logoUrl);
            }
            
            // Generate HTML report
            const response = await fetch(`${this.apiBaseUrl}/report/html?${params}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'text/plain',
                },
                body: code
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // Download the HTML report
            const htmlContent = await response.text();
            this.downloadFile(htmlContent, `code_review_report_${Date.now()}.html`, 'text/html');
            
            this.showSuccess('HTML report generated and downloaded successfully!');
            
        } catch (error) {
            console.error('Report generation failed:', error);
            this.showError(`Report generation failed: ${error.message}`);
        }
    }
    
    downloadHTMLReport() {
        this.generateReport();
    }
    
    downloadJSONReport() {
        if (!this.analysisResults) {
            this.showError('No analysis results to download.');
            return;
        }
        
        const jsonContent = JSON.stringify(this.analysisResults, null, 2);
        this.downloadFile(jsonContent, `code_review_${Date.now()}.json`, 'application/json');
        this.showSuccess('JSON report downloaded successfully!');
    }
    
    downloadFile(content, filename, contentType) {
        const blob = new Blob([content], { type: contentType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
    
    loadSampleCode() {
        const sampleCode = `def calculate_sum(a, b):
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
    
    # Security issue: unsafe file permissions
    os.chmod("/tmp/file", 0o777)  # B103: use of set_bad_file_permissions
    
    return "unsafe"

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
    print(f"Processed result: {result}")`;
        
        document.getElementById('codeInput').value = sampleCode;
        document.getElementById('filename').value = 'sample_code.py';
        this.updateButtonStates();
        this.highlightSyntax(document.getElementById('codeInput'));
    }
    
    hideResults() {
        const resultsContent = document.getElementById('resultsContent');
        const downloadSection = document.getElementById('downloadSection');
        const successMessage = document.getElementById('successMessage');
        
        resultsContent.classList.remove('show');
        downloadSection.style.display = 'none';
        successMessage.classList.remove('show');
    }
    
    showSuccess(message = 'Operation completed successfully!') {
        const successMessage = document.getElementById('successMessage');
        const messageElement = successMessage.querySelector('p');
        messageElement.textContent = message;
        successMessage.classList.add('show');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            successMessage.classList.remove('show');
        }, 5000);
    }
    
    showError(message) {
        // Create a temporary error message
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #fed7d7;
            color: #c53030;
            padding: 15px 20px;
            border-radius: 8px;
            border: 1px solid #feb2b2;
            z-index: 1000;
            max-width: 400px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
        
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}

// Initialize the application
const app = new CodeReviewApp();

// Global functions for HTML onclick handlers
function analyzeCode() {
    app.analyzeCode();
}

function generateReport() {
    app.generateReport();
}

function downloadHTMLReport() {
    app.downloadHTMLReport();
}

function downloadJSONReport() {
    app.downloadJSONReport();
}

function loadSampleCode() {
    app.loadSampleCode();
}
