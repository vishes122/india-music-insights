"""
Health check router
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..deps import get_database, get_cache
from ..schemas.charts import HealthResponse
from ..config import settings
from ..auth.spotify_token import token_manager

router = APIRouter(prefix="/v1", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(
    db: Session = Depends(get_database),
    cache = Depends(get_cache)
):
    """
    Health check endpoint
    
    Returns system status including:
    - API status
    - Database connectivity
    - Spotify API connectivity
    - Cache status
    - Last snapshot and aggregate dates
    """
    response = HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.version
    )
    
    # Check database connectivity
    try:
        db.execute(text("SELECT 1"))
        response.database = "connected"
    except Exception:
        response.database = "disconnected"
        response.status = "degraded"
    
    # Check Spotify API connectivity
    try:
        await token_manager.get_access_token()
        response.spotify_api = "connected"
    except Exception:
        response.spotify_api = "disconnected"
        response.status = "degraded"
    
    # Cache status
    try:
        cache_size = cache.size()
        response.cache_status = f"active ({cache_size} items)"
    except Exception:
        response.cache_status = "unavailable"
    
    # Get last snapshot date (from database)
    try:
        from ..models import PlaylistTrackSnapshot
        
        last_snapshot = db.query(PlaylistTrackSnapshot.snapshot_date)\
            .order_by(PlaylistTrackSnapshot.snapshot_date.desc())\
            .first()
        
        if last_snapshot:
            response.last_snapshot_date = last_snapshot[0]
    except Exception:
        pass
    
    # Get last aggregate computation date
    try:
        from ..models import YearlyTrackStats
        
        last_aggregate = db.query(YearlyTrackStats.last_computed_at)\
            .order_by(YearlyTrackStats.last_computed_at.desc())\
            .first()
        
        if last_aggregate:
            response.last_aggregate_date = last_aggregate[0].date()
    except Exception:
        pass
    
    return response
