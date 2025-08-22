#!/usr/bin/env python3
"""
Railway database setup script
Run this on Railway to populate the database with sample data
"""

import os
import sys
import asyncio
from datetime import datetime, date

# Add the app directory to the Python path
sys.path.insert(0, '/app')

from app.db import get_db_session, init_db
from app.models import Track, Artist, Playlist, PlaylistTrackSnapshot
from sqlalchemy.orm import Session

def add_railway_sample_data():
    """Add sample data to Railway database"""
    
    # Initialize database
    init_db()
    
    # Sample data
    sample_artists = [
        {"spotify_id": "artist1", "name": "Arijit Singh", "popularity": 95, "followers": 15000000},
        {"spotify_id": "artist2", "name": "Shreya Ghoshal", "popularity": 92, "followers": 8000000},
        {"spotify_id": "artist3", "name": "Vishal-Shekhar", "popularity": 88, "followers": 5000000},
        {"spotify_id": "artist4", "name": "Sachin-Jigar", "popularity": 85, "followers": 3000000}
    ]
    
    sample_tracks = [
        {
            "spotify_id": "track1",
            "name": "Kesariya",
            "album": "Brahmastra",
            "album_release_date": "2022-08-01",
            "popularity": 95,
            "explicit": False,
            "duration_ms": 240000
        },
        {
            "spotify_id": "track2", 
            "name": "Apna Bana Le",
            "album": "Bhediya",
            "popularity": 88,
            "explicit": False,
            "duration_ms": 220000
        },
        {
            "spotify_id": "track3",
            "name": "Tum Kya Mile",
            "album": "Rocky Aur Rani Kii Prem Kahaani",
            "popularity": 92,
            "explicit": False,
            "duration_ms": 280000
        },
        {
            "spotify_id": "track4",
            "name": "Ve Kamleya",
            "album": "Rocky Aur Rani Kii Prem Kahaani", 
            "popularity": 85,
            "explicit": False,
            "duration_ms": 260000
        }
    ]
    
    try:
        db = next(get_db_session())
        
        # Add artists
        for artist_data in sample_artists:
            artist = Artist(
                spotify_id=artist_data["spotify_id"],
                name=artist_data["name"],
                popularity=artist_data["popularity"],
                followers=artist_data["followers"]
            )
            db.add(artist)
        
        # Add tracks
        for track_data in sample_tracks:
            track = Track(
                spotify_id=track_data["spotify_id"],
                name=track_data["name"],
                album=track_data["album"],
                album_release_date=track_data["album_release_date"],
                popularity=track_data["popularity"],
                explicit=track_data["explicit"],
                duration_ms=track_data["duration_ms"]
            )
            db.add(track)
        
        # Add playlist
        playlist = Playlist(
            spotify_id="37i9dQZEVXbLZ52XmnySJg",
            name="India Top 50",
            market="IN"
        )
        db.add(playlist)
        
        db.commit()
        
        # Get the playlist and tracks back to create snapshots
        playlist = db.query(Playlist).filter_by(spotify_id="37i9dQZEVXbLZ52XmnySJg").first()
        tracks = db.query(Track).all()
        
        # Add playlist snapshots
        today = datetime.now().date()
        for i, track in enumerate(tracks):
            snapshot = PlaylistTrackSnapshot(
                playlist_id=playlist.id,
                track_id=track.id,
                snapshot_date=today,
                rank=i + 1,
                fetched_at=datetime.now()
            )
            db.add(snapshot)
        
        db.commit()
        print("✅ Sample data added successfully to Railway database!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_railway_sample_data()
