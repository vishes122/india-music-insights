"""
Charts API response schemas
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from .common import TrackOut, ArtistOut, YearlyGenreStatsOut, YearlyArtistStatsOut, YearlyTrackStatsOut


class ChartTrack(BaseModel):
    """Chart track with ranking information"""
    rank: int
    track_name: str
    artists: List[str]
    album: Optional[str] = None
    release_date: Optional[str] = None
    popularity: int
    spotify_url: Optional[str] = None
    preview_url: Optional[str] = None
    duration_formatted: Optional[str] = None
    explicit: bool = False


class TodayChartResponse(BaseModel):
    """Response for today's chart endpoint"""
    market: str
    snapshot_date: date
    total_tracks: int
    tracks: List[ChartTrack]
    last_updated: datetime


class YearlyChartResponse(BaseModel):
    """Response for yearly chart endpoint"""
    year: int
    market: str
    total_tracks: int
    tracks: List[YearlyTrackStatsOut]
    last_computed: Optional[datetime] = None


class TopGenresResponse(BaseModel):
    """Response for top genres endpoint"""
    year: int
    market: str
    total_genres: int
    genres: List[YearlyGenreStatsOut]
    last_computed: Optional[datetime] = None


class TopArtistsResponse(BaseModel):
    """Response for top artists endpoint"""
    year: int
    market: str
    total_artists: int
    artists: List[YearlyArtistStatsOut]
    last_computed: Optional[datetime] = None


class ArtistTopTracksResponse(BaseModel):
    """Response for artist top tracks endpoint"""
    artist_id: str
    artist_name: str
    market: str
    tracks: List[TrackOut]
    source: str = "spotify_live"  # spotify_live, database, mixed


class SearchResponse(BaseModel):
    """Response for search endpoint"""
    query: str
    search_type: str
    market: str
    total: int
    tracks: Optional[List[TrackOut]] = None
    artists: Optional[List[ArtistOut]] = None
    playlists: Optional[List[Dict[str, Any]]] = None
    source: str = "spotify_live"


class CompareGenresResponse(BaseModel):
    """Response for compare genres endpoint"""
    year: int
    markets: List[str]
    genres: List[Dict[str, Any]]  # Genre comparison data
    last_computed: Optional[datetime] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    timestamp: datetime
    version: str
    database: str = "connected"
    spotify_api: str = "connected"
    last_snapshot_date: Optional[date] = None
    last_aggregate_date: Optional[date] = None
    cache_status: str = "active"


class IngestResponse(BaseModel):
    """Ingest job response"""
    success: bool
    market: str
    snapshot_date: date
    tracks_processed: int
    artists_processed: int
    duration_seconds: float
    message: str


class AggregateResponse(BaseModel):
    """Aggregate computation response"""
    success: bool
    year: int
    market: str
    genres_computed: int
    artists_computed: int
    tracks_computed: int
    duration_seconds: float
    message: str


# Admin responses
class AdminResponse(BaseModel):
    """Generic admin operation response"""
    success: bool
    operation: str
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Error responses with specific error codes
class ValidationErrorResponse(BaseModel):
    """Validation error response"""
    success: bool = False
    error: str = "validation_error"
    message: str
    details: List[Dict[str, Any]]


class NotFoundErrorResponse(BaseModel):
    """Not found error response"""
    success: bool = False
    error: str = "not_found"
    message: str
    resource: str


class RateLimitErrorResponse(BaseModel):
    """Rate limit error response"""
    success: bool = False
    error: str = "rate_limit_exceeded"
    message: str
    retry_after: Optional[int] = None


class InternalErrorResponse(BaseModel):
    """Internal server error response"""
    success: bool = False
    error: str = "internal_error"
    message: str
    request_id: Optional[str] = None
