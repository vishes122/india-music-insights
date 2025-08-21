"""
Track, Artist, and related models
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Float, Text, JSON,
    ForeignKey, Table, Index, UniqueConstraint
)
from sqlalchemy.orm import relationship, Mapped

from .base import BaseModel


# Many-to-many association table for tracks and artists
track_artists = Table(
    'track_artists',
    BaseModel.metadata,
    Column('track_id', Integer, ForeignKey('tracks.id'), primary_key=True),
    Column('artist_id', Integer, ForeignKey('artists.id'), primary_key=True)
)


class Artist(BaseModel):
    """
    Artist model - represents a music artist from Spotify
    """
    __tablename__ = "artists"
    
    spotify_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    popularity = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    genres_json = Column(JSON, default=list)  # List of genre strings
    external_url = Column(String(500))
    image_url = Column(String(500))
    
    # Relationships
    tracks = relationship("Track", secondary=track_artists, back_populates="artists")
    yearly_stats = relationship("YearlyArtistStats", back_populates="artist")
    
    def __repr__(self):
        return f"<Artist(spotify_id='{self.spotify_id}', name='{self.name}')>"
    
    @property
    def genres(self) -> List[str]:
        """Get genres as a list"""
        return self.genres_json or []


class Track(BaseModel):
    """
    Track model - represents a music track from Spotify
    """
    __tablename__ = "tracks"
    
    spotify_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(500), nullable=False, index=True)
    album = Column(String(500))
    album_release_date = Column(String(20))  # YYYY-MM-DD format
    duration_ms = Column(Integer)
    explicit = Column(Boolean, default=False)
    popularity = Column(Integer, default=0)
    preview_url = Column(String(500))
    external_url = Column(String(500))
    
    # Audio features (can be added later)
    danceability = Column(Float)
    energy = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)
    
    # Relationships
    artists = relationship("Artist", secondary=track_artists, back_populates="tracks")
    playlist_snapshots = relationship("PlaylistTrackSnapshot", back_populates="track")
    yearly_stats = relationship("YearlyTrackStats", back_populates="track")
    
    def __repr__(self):
        return f"<Track(spotify_id='{self.spotify_id}', name='{self.name}')>"
    
    @property
    def artist_names(self) -> List[str]:
        """Get list of artist names"""
        return [artist.name for artist in self.artists]
    
    @property
    def release_year(self) -> Optional[int]:
        """Extract year from album release date"""
        if self.album_release_date:
            try:
                return int(self.album_release_date[:4])
            except (ValueError, IndexError):
                pass
        return None


class Genre(BaseModel):
    """
    Genre model - normalized genre names
    """
    __tablename__ = "genres"
    
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    def __repr__(self):
        return f"<Genre(name='{self.name}')>"


class Playlist(BaseModel):
    """
    Playlist model - represents Spotify playlists we track
    """
    __tablename__ = "playlists"
    
    spotify_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(500), nullable=False)
    market = Column(String(5), nullable=False, index=True)  # "IN", "US", etc.
    description = Column(Text)
    external_url = Column(String(500))
    image_url = Column(String(500))
    
    # Relationships
    snapshots = relationship("PlaylistTrackSnapshot", back_populates="playlist")
    
    __table_args__ = (
        Index('idx_playlist_market', 'market'),
    )
    
    def __repr__(self):
        return f"<Playlist(spotify_id='{self.spotify_id}', name='{self.name}', market='{self.market}')>"


class PlaylistTrackSnapshot(BaseModel):
    """
    Playlist track snapshot - captures the state of a playlist on a specific date
    """
    __tablename__ = "playlist_track_snapshots"
    
    playlist_id = Column(Integer, ForeignKey('playlists.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    snapshot_date = Column(DateTime, nullable=False, index=True)
    rank = Column(Integer, nullable=False)  # Position in playlist (1-50)
    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Additional metadata
    added_at = Column(DateTime)  # When track was added to playlist (from Spotify)
    
    # Relationships
    playlist = relationship("Playlist", back_populates="snapshots")
    track = relationship("Track", back_populates="playlist_snapshots")
    
    __table_args__ = (
        UniqueConstraint('playlist_id', 'track_id', 'snapshot_date', name='uq_playlist_track_snapshot'),
        Index('idx_snapshot_date_rank', 'snapshot_date', 'rank'),
        Index('idx_playlist_snapshot', 'playlist_id', 'snapshot_date'),
    )
    
    def __repr__(self):
        return f"<PlaylistTrackSnapshot(playlist_id={self.playlist_id}, track_id={self.track_id}, rank={self.rank}, date={self.snapshot_date})>"
