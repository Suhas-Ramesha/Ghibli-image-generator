# 🚀 Deployment Guide - Ghibli Image Generator

This guide covers deployment to the specific platforms requested: **Hugging Face Spaces** for backend and **Vercel/Netlify** for frontend.

## 🎯 Architecture Overview

```
Frontend (Vercel/Netlify) ←→ Backend (Hugging Face Spaces)
```

## 🤗 Backend Deployment - Hugging Face Spaces

### Option 1: Hugging Face Spaces (Recommended)

1. **Create a new Space**:
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose:
     - **Space name**: `ghibli-image-generator`
     - **License**: `MIT`
     - **SDK**: `Gradio`
     - **Hardware**: `CPU basic` (free) or `GPU T4 small` (paid)

2. **Upload files**:
   ```bash
   # Clone your space repository
   git clone https://huggingface.co/spaces/YOUR_USERNAME/ghibli-image-generator
   cd ghibli-image-generator
   
   # Copy backend files
   cp /path/to/your/backend/app.py .
   cp /path/to/your/backend/requirements-hf.txt requirements.txt
   cp /path/to/your/backend/README.md .
   
   # Commit and push
   git add .
   git commit -m "Initial deployment"
   git push
   ```

3. **Set environment variables** (if using HF API):
   - Go to your Space settings
   - Add `HUGGINGFACE_TOKEN` with your token value

4. **Your backend will be available at**:
   ```
   https://YOUR_USERNAME-ghibli-image-generator.hf.space
   ```

### Option 2: Render with GPU (Alternative)

1. **Create account** at [Render](https://render.com)

2. **Create Web Service**:
   - Connect your GitHub repository
   - Set **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Instance Type**: Choose GPU instance

3### 2. Set Environment Variables

- **HUGGINGFACE_TOKEN**: This is crucial for the backend to authenticate with the Hugging Face Inference API. You can obtain your token from your [Hugging Face profile settings](https://huggingface.co/settings/tokens). Add this as a secret environment variable in your Hugging Face Space settings or Render environment variables.
- **PORT**: `10000` (for Render deployment)# 🌐 Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

3. **Configure Environment Variables**:
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add:
     ```
     VITE_API_URL = https://YOUR_USERNAME-ghibli-image-generator.hf.space
     ```

4. **Redeploy**:
   ```bash
   vercel --prod
   ```

### Option 2: Netlify (Alternative)

1. **Build the frontend**:
   ```bash
   cd frontend
   pnpm run build
   ```

2. **Deploy via Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   netlify deploy --prod --dir=dist
   ```

3. **Or deploy via Git**:
   - Connect your GitHub repository to Netlify
   - Set **Build command**: `cd frontend && pnpm run build`
   - Set **Publish directory**: `frontend/dist`
   - Add environment variable: `VITE_API_URL`

## 🔧 Configuration Steps

### 1. Update Frontend API URL

In your frontend `.env.production`:
```env
VITE_API_URL=https://YOUR_USERNAME-ghibli-image-generator.hf.space
```

### 2. Enable CORS in Backend

The Gradio app automatically handles CORS, but if using Flask:
```python
from flask_cors import CORS
CORS(app, origins=["https://your-frontend-domain.vercel.app"])
```

### 3. Test the Connection

1. Deploy backend first and get the URL
2. Update frontend environment variable
3. Deploy frontend
4. Test image upload and conversion

## 📋 Deployment Checklist

### Backend (Hugging Face Spaces)
- [ ] Space created with correct settings
- [ ] `app.py` uploaded
- [ ] `requirements.txt` uploaded
- [ ] `README.md` uploaded with proper metadata
- [ ] Environment variables set (if needed)
- [ ] Space is running and accessible

### Frontend (Vercel/Netlify)
- [ ] Project connected to Git repository
- [ ] Build settings configured
- [ ] Environment variables set
- [ ] API URL pointing to backend
- [ ] Deployment successful
- [ ] CORS working properly

## 🚀 Quick Deploy Commands

### Complete Deployment Script

```bash
#!/bin/bash

# 1. Deploy to Hugging Face Spaces
echo "🤗 Deploying to Hugging Face Spaces..."
cd backend
# Manual upload required - see HF Spaces documentation

# 2. Deploy to Vercel
echo "▲ Deploying to Vercel..."
cd ../frontend
vercel --prod

echo "✅ Deployment complete!"
echo "Frontend: Check Vercel dashboard for URL"
echo "Backend: https://YOUR_USERNAME-ghibli-image-generator.hf.space"
```

## 🔍 Troubleshooting

### Common Issues

**1. CORS Errors**
```javascript
// Frontend: Ensure API URL is correct
const API_URL = import.meta.env.VITE_API_URL || '';
```

**2. Hugging Face Spaces Not Starting**
- Check `requirements.txt` for correct versions
- Verify `app.py` has proper Gradio interface
- Check logs in HF Spaces interface

**3. Environment Variables Not Loading**
- Restart the service after adding variables
- Check variable names match exactly
- Use platform-specific variable setting methods

**4. Build Failures**
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

## 💰 Cost Breakdown

| Service | Free Tier | Paid Options |
|---------|-----------|--------------|
| **HF Spaces** | CPU Basic (Free) | GPU T4 Small ($0.60/hour) |
| **Vercel** | 100GB bandwidth | Pro ($20/month) |
| **Netlify** | 100GB bandwidth | Pro ($19/month) |
| **Render** | 750 hours/month | GPU instances ($0.50+/hour) |

## 🎯 Production Recommendations

### For Free Deployment
- **Backend**: Hugging Face Spaces (CPU)
- **Frontend**: Vercel or Netlify
- **Total Cost**: $0/month

### For Better Performance
- **Backend**: Hugging Face Spaces (GPU T4)
- **Frontend**: Vercel Pro
- **Total Cost**: ~$20-50/month

### For High Traffic
- **Backend**: Render GPU or AWS/GCP
- **Frontend**: Vercel Pro with CDN
- **Database**: Add Redis for caching
- **Total Cost**: $100+/month

## 📞 Support

If you encounter issues:

1. **Hugging Face Spaces**: Check [HF Spaces documentation](https://huggingface.co/docs/hub/spaces)
2. **Vercel**: Check [Vercel documentation](https://vercel.com/docs)
3. **Netlify**: Check [Netlify documentation](https://docs.netlify.com)

---

🎨 **Happy Deploying!** Your Ghibli Image Generator will be live and ready to transform photos into magical artwork!

