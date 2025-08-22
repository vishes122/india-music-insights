# 🚨 Backend Data Setup Required

## Current Issue
Your frontend is working correctly, but the backend database is empty! The API endpoints exist but have no data to return.

## Required Steps to Fix

### 1. Configure Railway Environment Variables
In your Railway dashboard, you need to set these environment variables:

```bash
# Get these from Spotify Developer Dashboard
SPOTIFY_CLIENT_ID=your_actual_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_actual_spotify_client_secret

# Generate a secure admin key  
ADMIN_KEY=your_secure_random_admin_key_here

# Your Vercel domain (once you have it)
CORS_ORIGINS=https://your-vercel-domain.vercel.app,http://localhost:3000,http://localhost:5173

# These should already be set
MARKETS=IN,US,GB
INDIA_TOP50_PLAYLIST_ID=37i9dQZEVXbLZ52XmnySJg
GLOBAL_TOP50_PLAYLIST_ID=37i9dQZEVXbMDoHDwVN2tF
TIMEZONE=Asia/Kolkata
ENABLE_SCHEDULER=True
```

### 2. Get Spotify API Credentials
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create an app or use existing one
3. Copy Client ID and Client Secret
4. Add them to Railway environment variables

### 3. Run Data Ingestion
After setting up the environment variables, trigger data ingestion:

```bash
# Using curl (replace YOUR_ADMIN_KEY with actual key)
curl -X POST "https://web-production-ca268.up.railway.app/v1/admin/ingest/run" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: YOUR_ADMIN_KEY"
```

Or visit: `https://web-production-ca268.up.railway.app/docs` and use the interactive API docs.

### 4. Verify Data
After ingestion, test these endpoints:
- `https://web-production-ca268.up.railway.app/v1/analytics/overview?market=IN`
- `https://web-production-ca268.up.railway.app/v1/charts/top-today?market=IN`

## Quick Test Commands

```bash
# Test if overview has data (should show non-zero counts)
curl "https://web-production-ca268.up.railway.app/v1/analytics/overview?market=IN"

# Test if charts have data  
curl "https://web-production-ca268.up.railway.app/v1/charts/top-today?market=IN"
```

## Alternative: Add Sample Data
If you can't get Spotify API access immediately, you can add sample data locally and then deploy.

## Status Check
- ✅ Backend deployed and running
- ✅ Frontend routing fixed
- ❌ Database empty (needs data ingestion)
- ❌ Spotify credentials needed
- ❌ Admin key needed for data ingestion
