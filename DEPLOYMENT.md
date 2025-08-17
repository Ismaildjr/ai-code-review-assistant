# 🚀 Deployment Guide

## Render Deployment Checklist

### ✅ Pre-Deployment
- [ ] All tests pass locally (`pytest tests/ -v`)
- [ ] Code is committed to GitHub
- [ ] Environment variables are configured
- [ ] API keys are ready (if using AI features)

### 🔧 Render Setup

#### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub account

#### 2. Create New Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select the repository: `ai-code-review-assistant`

#### 3. Configure Service
- **Name**: `ai-code-review-assistant` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

#### 4. Environment Variables
```bash
# Required
PORT=8000

# Optional (for production)
LOG_LEVEL=INFO
DEBUG=false
RELOAD=false

# AI Features (if using)
HF_TOKEN=your_huggingface_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

#### 5. Advanced Settings
- **Health Check Path**: `/`
- **Auto-Deploy**: Enable for automatic deployments
- **Plan**: Start with Free plan, upgrade as needed

### 🚀 Deploy
1. Click "Create Web Service"
2. Wait for build to complete (usually 2-5 minutes)
3. Your app will be available at: `https://your-app-name.onrender.com`

### 🔍 Post-Deployment Verification
- [ ] Health check passes (`/` endpoint)
- [ ] Main UI loads (`/ui` endpoint)
- [ ] API documentation accessible (`/docs` endpoint)
- [ ] Static analysis tools work
- [ ] AI review features work (if configured)

### 📊 Monitoring
- **Logs**: Available in Render dashboard
- **Metrics**: Response times, error rates
- **Health**: Automatic health checks

### 🔄 Updates
- **Automatic**: Push to GitHub triggers auto-deploy
- **Manual**: Use "Manual Deploy" button in dashboard

### 🆘 Troubleshooting

#### Common Issues
1. **Build fails**: Check requirements.txt and Python version
2. **App won't start**: Verify start command and environment variables
3. **Health check fails**: Check if app is listening on correct port
4. **Static files not loading**: Verify static directory structure

#### Debug Commands
```bash
# Check logs in Render dashboard
# Test locally with same environment
export PORT=8000
python api.py
```

### 💰 Cost Optimization
- **Free Plan**: 750 hours/month, sleeps after 15 minutes of inactivity
- **Paid Plans**: Always-on, better performance, custom domains
- **Auto-scaling**: Available on paid plans

### 🔐 Security
- **HTTPS**: Automatically provided by Render
- **Environment Variables**: Secure storage for API keys
- **CORS**: Configured for web access
- **Rate Limiting**: Consider adding for production use

## 🎯 Next Steps
1. Deploy to Render
2. Test all functionality
3. Configure custom domain (optional)
4. Set up monitoring and alerts
5. Share your deployed app!

## 📞 Support
- **Render Docs**: [docs.render.com](https://docs.render.com)
- **Render Support**: Available in dashboard
- **Project Issues**: GitHub repository issues
