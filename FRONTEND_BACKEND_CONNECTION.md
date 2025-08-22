# Frontend-Backend Connection Setup

## Current Status
- ✅ Backend deployed on Railway: https://web-production-ca268.up.railway.app
- ✅ Frontend configured for Vercel deployment
- ⚠️ Need to connect them properly

## Steps to Complete the Connection

### 1. Get Your Vercel Deployment URL
After deploying to Vercel, you'll get a URL like: `https://your-project-name-hash.vercel.app`

### 2. Update Railway Environment Variables
In your Railway dashboard, add/update the following environment variable:
```
CORS_ORIGINS=https://your-vercel-domain.vercel.app,http://localhost:3000,http://localhost:5173
```

Replace `your-vercel-domain.vercel.app` with your actual Vercel URL.

### 3. Redeploy Backend (if needed)
Railway should automatically redeploy when you update environment variables.

### 4. Test the Connection
Visit your Vercel frontend and check if it can connect to the Railway backend.

## Files Updated
- ✅ `frontend/indie-melody-pulse-89/.env.production` - Added production API URL
- ✅ `frontend/indie-melody-pulse-89/vercel.json` - Added environment variable
- ✅ `india-music-insights/app/main.py` - Updated CORS configuration  
- ✅ `india-music-insights/app/config.py` - Added CORS origins setting

## Frontend Environment Variables
The frontend now uses:
- **Development**: `VITE_API_BASE_URL=http://localhost:8000`
- **Production**: `VITE_API_BASE_URL=https://web-production-ca268.up.railway.app`

## Backend CORS Configuration
The backend now accepts requests from:
- Development: localhost ports (3000, 5173, 8080)
- Production: URLs specified in `CORS_ORIGINS` environment variable

## Next Steps
1. Get your Vercel deployment URL
2. Update Railway's CORS_ORIGINS environment variable
3. Test the connection
4. If issues persist, check browser console for CORS errors
