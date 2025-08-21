"""
Aggregate models for yearly statistics
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey,
    Index, UniqueConstraint
)
from sqlalchemy.orm import relationship

from .base import BaseModel


class YearlyGenreStats(BaseModel):
    """
    Yearly statistics for genres by market
    """
    __tablename__ = "yearly_genre_stats"
    
    year = Column(Integer, nullable=False, index=True)
    market = Column(String(5), nullable=False, index=True)
    genre_name = Column(String(100), nullable=False, index=True)
    track_count = Column(Integer, default=0)
    avg_popularity = Column(Float, default=0.0)
    total_appearances = Column(Integer, default=0)  # Total playlist appearances
    
    # Top track for this genre/year/market
    top_track_spotify_id = Column(String(50))
    top_track_name = Column(String(500))
    top_track_avg_rank = Column(Float)
    
    last_computed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('year', 'market', 'genre_name', name='uq_yearly_genre'),
        Index('idx_genre_year_market', 'year', 'market'),
    )
    
    def __repr__(self):
        return f"<YearlyGenreStats(year={self.year}, market='{self.market}', genre='{self.genre_name}')>"


class YearlyArtistStats(BaseModel):
    """
    Yearly statistics for artists by market
    """
    __tablename__ = "yearly_artist_stats"
    
    year = Column(Integer, nullable=False, index=True)
    market = Column(String(5), nullable=False, index=True)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)
    artist_name = Column(String(255), nullable=False)  # Denormalized for easier queries
    track_count = Column(Integer, default=0)
    avg_popularity = Column(Float, default=0.0)
    total_appearances = Column(Integer, default=0)
    
    # Top track for this artist/year/market
    top_track_spotify_id = Column(String(50))
    top_track_name = Column(String(500))
    top_track_avg_rank = Column(Float)
    top_track_best_rank = Column(Integer)
    
    last_computed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    artist = relationship("Artist", back_populates="yearly_stats")
    
    __table_args__ = (
        UniqueConstraint('year', 'market', 'artist_id', name='uq_yearly_artist'),
        Index('idx_artist_year_market', 'year', 'market'),
    )
    
    def __repr__(self):
        return f"<YearlyArtistStats(year={self.year}, market='{self.market}', artist='{self.artist_name}')>"


class YearlyTrackStats(BaseModel):
    """
    Yearly statistics for tracks by market
    """
    __tablename__ = "yearly_track_stats"
    
    year = Column(Integer, nullable=False, index=True)
    market = Column(String(5), nullable=False, index=True)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    track_name = Column(String(500), nullable=False)  # Denormalized
    appearances = Column(Integer, default=0)  # Number of times appeared in charts
    avg_rank = Column(Float)  # Average ranking position
    best_rank = Column(Integer)  # Best (lowest number) ranking
    worst_rank = Column(Integer)  # Worst (highest number) ranking
    popularity = Column(Integer, default=0)  # Latest popularity score
    
    # Time-based metrics
    first_appearance = Column(DateTime)
    last_appearance = Column(DateTime)
    days_on_chart = Column(Integer, default=0)
    
    last_computed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    track = relationship("Track", back_populates="yearly_stats")
    
    __table_args__ = (
        UniqueConstraint('year', 'market', 'track_id', name='uq_yearly_track'),
        Index('idx_track_year_market', 'year', 'market'),
        Index('idx_track_avg_rank', 'year', 'market', 'avg_rank'),
    )
    
    def __repr__(self):
        return f"<YearlyTrackStats(year={self.year}, market='{self.market}', track='{self.track_name}')>"
