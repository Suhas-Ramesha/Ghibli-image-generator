# 🚀 Deployment Guide - Ghibli Image Generator

This comprehensive guide covers multiple free deployment options for your Ghibli Image Generator application. Choose the option that best fits your needs.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Tested the application locally
- [ ] All dependencies listed in requirements.txt and package.json
- [ ] Environment variables configured
- [ ] Git repository set up
- [ ] Hugging Face token (optional but recommended)

## 🌟 Option 1: Render (Recommended - Completely Free)

Render offers free hosting for both frontend and backend with automatic deployments from GitHub.

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Create a render.yaml file** in your project root:
```yaml
services:
  - type: web
    name: ghibli-backend
    env: python
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && python src/main.py"
    envVars:
      - key: HUGGINGFACE_TOKEN
        value: your_token_here
      - key: PORT
        value: 10000
```

### Step 2: Deploy Backend on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `ghibli-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Instance Type**: `Free`

5. Add Environment Variables:
   - `HUGGINGFACE_TOKEN`: Your HF token (optional)
   - `PORT`: `10000`

6. Click "Create Web Service"

### Step 3: Build and Deploy Frontend

1. **Update API URL in frontend**:
```javascript
// In frontend/src/App.jsx, update the fetch URL
const response = await fetch('https://your-backend-url.onrender.com/api/ghibli/convert', {
  method: 'POST',
  body: formData
})
```

2. **Build the frontend**:
```bash
cd frontend
pnpm run build
```

3. **Copy build files to backend static folder**:
```bash
cp -r dist/* ../backend/src/static/
```

4. **Commit and push changes**:
```bash
git add .
git commit -m "Add production build"
git push origin main
```

The backend service will automatically redeploy and serve both API and frontend.

## 🔥 Option 2: Vercel + Railway

This option separates frontend and backend deployment for better scalability.

### Frontend Deployment (Vercel)

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Deploy frontend**:
```bash
cd frontend
vercel
```

3. **Configure build settings**:
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `pnpm run build`
   - Output Directory: `dist`

4. **Set environment variables** in Vercel dashboard:
   - `VITE_API_URL`: Your Railway backend URL

### Backend Deployment (Railway)

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login and deploy**:
```bash
railway login
railway new
railway link
cd backend
railway up
```

3. **Configure environment variables**:
```bash
railway variables set HUGGINGFACE_TOKEN=your_token_here
```

## ⚡ Option 3: Netlify + Heroku

### Frontend Deployment (Netlify)

1. **Build the frontend**:
```bash
cd frontend
pnpm run build
```

2. **Deploy to Netlify**:
   - Drag and drop the `dist` folder to [Netlify Drop](https://app.netlify.com/drop)
   - Or connect your GitHub repository for automatic deployments

3. **Configure build settings**:
   - Build command: `cd frontend && pnpm run build`
   - Publish directory: `frontend/dist`

### Backend Deployment (Heroku)

1. **Install Heroku CLI** and login:
```bash
heroku login
```

2. **Create Heroku app**:
```bash
cd backend
heroku create your-app-name
```

3. **Create Procfile**:
```bash
echo "web: python src/main.py" > Procfile
```

4. **Set environment variables**:
```bash
heroku config:set HUGGINGFACE_TOKEN=your_token_here
heroku config:set PORT=$PORT
```

5. **Deploy**:
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 🐳 Option 4: Docker Deployment

### Create Dockerfile for Backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/

EXPOSE 5000

CMD ["python", "src/main.py"]
```

### Create Dockerfile for Frontend

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - HUGGINGFACE_TOKEN=${HUGGINGFACE_TOKEN}
    
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

### Deploy with Docker

```bash
# Build and run
docker-compose up --build

# Deploy to cloud platforms that support Docker
# (DigitalOcean App Platform, Google Cloud Run, etc.)
```

## 🔧 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `HUGGINGFACE_TOKEN` | HuggingFace API token (optional) | `hf_xxxxxxxxxxxxx` |
| `PORT` | Port for backend server | `5000` |
| `FLASK_ENV` | Flask environment | `production` |

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://api.yourapp.com` |

## 🔍 Monitoring and Maintenance

### Health Checks

Most platforms support health checks. Use this endpoint:
```
GET /api/ghibli/health
```

### Logging

Monitor your application logs:

**Render**: Dashboard → Service → Logs
**Heroku**: `heroku logs --tail`
**Railway**: `railway logs`
**Vercel**: Dashboard → Functions → View Function Logs

### Performance Optimization

1. **Enable gzip compression**
2. **Use CDN for static assets**
3. **Implement caching headers**
4. **Monitor response times**

## 🚨 Troubleshooting Deployment Issues

### Common Problems

**1. Build Failures**
```bash
# Check build logs
# Ensure all dependencies are in requirements.txt/package.json
# Verify Python/Node versions
```

**2. CORS Issues**
```python
# Ensure CORS is properly configured in Flask
from flask_cors import CORS
CORS(app)
```

**3. Environment Variables Not Loading**
```bash
# Check variable names match exactly
# Restart services after adding variables
# Use platform-specific variable setting methods
```

**4. Static Files Not Serving**
```python
# Verify static folder path in Flask
app = Flask(__name__, static_folder='static')
```

### Platform-Specific Issues

**Render**:
- Free tier has 750 hours/month limit
- Services sleep after 15 minutes of inactivity
- Build time limit: 20 minutes

**Heroku**:
- Free tier discontinued (use alternatives)
- Dynos sleep after 30 minutes of inactivity
- Ephemeral filesystem

**Vercel**:
- Function timeout: 10 seconds (Hobby plan)
- Serverless functions only
- No persistent storage

## 📊 Cost Comparison

| Platform | Frontend | Backend | Database | Total/Month |
|----------|----------|---------|----------|-------------|
| Render | Free | Free | Free (PostgreSQL) | $0 |
| Vercel + Railway | Free | Free | Free | $0 |
| Netlify + Heroku | Free | $7+ | $9+ | $16+ |
| DigitalOcean | $5+ | $5+ | $15+ | $25+ |

## 🎯 Production Recommendations

### For Small Projects (< 1000 users/month)
- **Render**: Single service deployment
- **Vercel + Railway**: Separated concerns

### For Medium Projects (1000-10000 users/month)
- **DigitalOcean App Platform**
- **Google Cloud Run**
- **AWS Elastic Beanstalk**

### For Large Projects (10000+ users/month)
- **AWS ECS/EKS**
- **Google Kubernetes Engine**
- **Azure Container Instances**

## 🔐 Security Considerations

1. **Environment Variables**: Never commit tokens to Git
2. **HTTPS**: Ensure all deployments use HTTPS
3. **CORS**: Configure properly for production domains
4. **Rate Limiting**: Implement to prevent abuse
5. **Input Validation**: Validate file uploads
6. **Error Handling**: Don't expose sensitive information

## 📈 Scaling Strategies

### Horizontal Scaling
- Use load balancers
- Deploy multiple instances
- Implement session management

### Vertical Scaling
- Increase server resources
- Optimize code performance
- Use caching strategies

### Database Scaling
- Use connection pooling
- Implement read replicas
- Consider NoSQL for specific use cases

---

Choose the deployment option that best fits your needs and budget. Start with free tiers and scale up as your application grows! 🚀

