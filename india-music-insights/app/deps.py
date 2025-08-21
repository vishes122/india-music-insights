"""
Dependency injection for FastAPI routes
"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from .db import get_db
from .config import settings
from .clients.spotify import SpotifyClient
from .utils.caching import cache
from .utils.logging import get_request_logger


def get_database() -> Generator[Session, None, None]:
    """
    Get database session dependency
    
    Yields:
        Database session
    """
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


async def get_spotify_client():
    """
    Get Spotify API client dependency
    
    Yields:
        Configured Spotify client
    """
    async with SpotifyClient() as client:
        yield client


def get_cache():
    """
    Get cache instance dependency
    
    Returns:
        Cache instance
    """
    return cache


def get_logger():
    """
    Get logger dependency
    
    Returns:
        Configured logger
    """
    return get_request_logger()


def verify_admin_key(x_admin_key: Optional[str] = Header(None)):
    """
    Verify admin API key
    
    Args:
        x_admin_key: Admin key from header
        
    Raises:
        HTTPException: If key is invalid or missing
    """
    if not x_admin_key or x_admin_key != settings.admin_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing admin key"
        )
    return True


def validate_market(market: str = "IN") -> str:
    """
    Validate market parameter
    
    Args:
        market: Market code
        
    Returns:
        Validated market code
        
    Raises:
        HTTPException: If market is invalid
    """
    market = market.upper()
    
    if market not in settings.markets:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid market '{market}'. Supported markets: {', '.join(settings.markets)}"
        )
    
    return market


def validate_year(year: int) -> int:
    """
    Validate year parameter
    
    Args:
        year: Year value
        
    Returns:
        Validated year
        
    Raises:
        HTTPException: If year is invalid
    """
    from datetime import datetime
    current_year = datetime.now().year
    
    # Allow historical searches back to 1900 and future to current_year + 1
    if year < 1900 or year > current_year + 1:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid year '{year}'. Must be between 1900 and {current_year + 1}"
        )
    
    return year


def validate_limit(limit: int = 50) -> int:
    """
    Validate limit parameter
    
    Args:
        limit: Limit value
        
    Returns:
        Validated limit
        
    Raises:
        HTTPException: If limit is invalid
    """
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )
    
    return limit


def validate_search_type(search_type: str = "track") -> str:
    """
    Validate search type parameter
    
    Args:
        search_type: Search type
        
    Returns:
        Validated search type
        
    Raises:
        HTTPException: If search type is invalid
    """
    valid_types = ["track", "artist", "album", "playlist"]
    
    if search_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid search type '{search_type}'. Supported types: {', '.join(valid_types)}"
        )
    
    return search_type


# Common dependency combinations
CommonDeps = {
    "db": Depends(get_database),
    "spotify": Depends(get_spotify_client),
    "cache": Depends(get_cache),
    "logger": Depends(get_logger),
}

AdminDeps = {
    **CommonDeps,
    "admin_verified": Depends(verify_admin_key),
}
