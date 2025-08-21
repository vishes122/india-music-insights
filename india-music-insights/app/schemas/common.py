"""
Common Pydantic schemas for API responses
"""

from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, computed_field


class ArtistOut(BaseModel):
    """Artist output schema"""
    spotify_id: str
    name: str
    popularity: int = 0
    followers: int = 0
    genres: List[str] = Field(default_factory=list)
    external_url: Optional[str] = None
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class TrackOut(BaseModel):
    """Track output schema"""
    spotify_id: str
    name: str
    artists: List[ArtistOut] = Field(default_factory=list)
    album: Optional[str] = None
    album_release_date: Optional[str] = None
    duration_ms: Optional[int] = None
    explicit: bool = False
    popularity: int = 0
    preview_url: Optional[str] = None
    external_url: Optional[str] = None
    
    # Computed fields
    @computed_field
    @property
    def duration_formatted(self) -> Optional[str]:
        """Format duration from milliseconds"""
        if not self.duration_ms:
            return "0:00"
        
        seconds = self.duration_ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    @computed_field
    @property
    def artist_names(self) -> List[str]:
        """Extract artist names from artists list"""
        return [artist.name for artist in self.artists]
    
    @computed_field
    @property
    def release_year(self) -> Optional[int]:
        """Extract year from release date"""
        if self.album_release_date:
            try:
                return int(self.album_release_date[:4])
            except (ValueError, IndexError):
                pass
        return None
    
    class Config:
        from_attributes = True


class GenreOut(BaseModel):
    """Genre output schema"""
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class PlaylistOut(BaseModel):
    """Playlist output schema"""
    spotify_id: str
    name: str
    market: str
    description: Optional[str] = None
    external_url: Optional[str] = None
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class PlaylistTrackSnapshotOut(BaseModel):
    """Playlist track snapshot output schema"""
    rank: int
    snapshot_date: datetime
    track: TrackOut
    added_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Aggregate schemas
class YearlyGenreStatsOut(BaseModel):
    """Yearly genre statistics output schema"""
    year: int
    market: str
    genre_name: str
    track_count: int
    avg_popularity: float
    total_appearances: int
    top_track_spotify_id: Optional[str] = None
    top_track_name: Optional[str] = None
    top_track_avg_rank: Optional[float] = None
    last_computed_at: datetime
    
    class Config:
        from_attributes = True


class YearlyArtistStatsOut(BaseModel):
    """Yearly artist statistics output schema"""
    year: int
    market: str
    artist_name: str
    track_count: int
    avg_popularity: float
    total_appearances: int
    top_track_spotify_id: Optional[str] = None
    top_track_name: Optional[str] = None
    top_track_avg_rank: Optional[float] = None
    top_track_best_rank: Optional[int] = None
    last_computed_at: datetime
    
    class Config:
        from_attributes = True


class YearlyTrackStatsOut(BaseModel):
    """Yearly track statistics output schema"""
    year: int
    market: str
    track_name: str
    appearances: int
    avg_rank: Optional[float] = None
    best_rank: Optional[int] = None
    worst_rank: Optional[int] = None
    popularity: int
    days_on_chart: int = 0
    first_appearance: Optional[datetime] = None
    last_appearance: Optional[datetime] = None
    track: Optional[TrackOut] = None
    
    class Config:
        from_attributes = True


# Pagination
class PaginationMeta(BaseModel):
    """Pagination metadata"""
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel):
    """Generic paginated response"""
    data: List[BaseModel]
    meta: PaginationMeta


# Common response wrappers
class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    message: str
    data: Optional[BaseModel] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: str
    details: Optional[dict] = None
