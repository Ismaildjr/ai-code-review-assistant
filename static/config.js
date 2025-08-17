// Configuration for different environments
const config = {
    // Development
    development: {
        apiBaseUrl: 'http://localhost:8000'
    },
    // Production (Render)
    production: {
        apiBaseUrl: window.location.origin
    }
};

// Auto-detect environment
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const currentConfig = isDevelopment ? config.development : config.production;

// Export for use in other files
window.appConfig = currentConfig;
