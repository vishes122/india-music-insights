"""
Database models for India Music Insights
"""

from .base import BaseModel
from .track import Artist, Track, Genre, Playlist, PlaylistTrackSnapshot, track_artists
from .aggregates import YearlyGenreStats, YearlyArtistStats, YearlyTrackStats

__all__ = [
    "BaseModel",
    "Artist",
    "Track", 
    "Genre",
    "Playlist",
    "PlaylistTrackSnapshot",
    "track_artists",
    "YearlyGenreStats",
    "YearlyArtistStats", 
    "YearlyTrackStats",
]
