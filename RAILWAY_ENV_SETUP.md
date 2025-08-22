# Railway Environment Variables Setup

## Critical: Add these environment variables to your Railway deployment

Go to your Railway project dashboard → Settings → Environment Variables

Add these variables:

```
SPOTIFY_CLIENT_ID=6d1427d315ff436eb9fe8fc1c7c411fa
SPOTIFY_CLIENT_SECRET=29a5d7ca90dc4602ae7bc759c937079d
ADMIN_KEY=india_music_insights_admin_2025
INDIA_TOP50_PLAYLIST_ID=37i9dQZEVXbLZ52XmnySJg
GLOBAL_TOP50_PLAYLIST_ID=37i9dQZEVXbMDoHDwVN2tF
MARKETS=IN,US,GB
ENV=production
LOG_LEVEL=INFO
TIMEZONE=Asia/Kolkata
DATABASE_URL=sqlite:///./india_music_insights.db
ENABLE_SCHEDULER=True
```

## Important Notes:
1. **INDIA_TOP50_PLAYLIST_ID**: I'm using the official Spotify "Top 50 - India" playlist ID: `37i9dQZEVXbLZ52XmnySJg`
2. After adding these variables, Railway will automatically redeploy
3. Once deployed, the real Spotify Top 50 data will be automatically fetched

## Test After Deployment:
```bash
# This will fetch real Top 50 India tracks from Spotify
curl -X POST "https://web-production-ca268.up.railway.app/v1/admin/ingest/run?market=IN" \
  -H "X-Admin-Key: india_music_insights_admin_2025"
```
