#!/usr/bin/env python3
"""
Sample data loader for testing the dashboard without Spotify API
"""

import sqlite3
import json
from datetime import datetime, date

def add_sample_data():
    """Add sample tracks to the database for testing"""
    
    # Sample track data
    sample_tracks = [
        {
            "id": "track1",
            "name": "Kesariya",
            "album_id": "album1",
            "album_name": "Brahmastra",
            "popularity": 95,
            "external_spotify_url": "https://open.spotify.com/track/1",
            "release_date": "2022-08-01"
        },
        {
            "id": "track2", 
            "name": "Apna Bana Le",
            "album_id": "album2",
            "album_name": "Bhediya",
            "popularity": 88,
            "external_spotify_url": "https://open.spotify.com/track/2",
            "release_date": "2022-11-15"
        },
        {
            "id": "track3",
            "name": "Tum Kya Mile",
            "album_id": "album3", 
            "album_name": "Rocky Aur Rani Kii Prem Kahaani",
            "popularity": 92,
            "external_spotify_url": "https://open.spotify.com/track/3",
            "release_date": "2023-07-10"
        },
        {
            "id": "track4",
            "name": "Ve Kamleya",
            "album_id": "album4",
            "album_name": "Rocky Aur Rani Kii Prem Kahaani", 
            "popularity": 85,
            "external_spotify_url": "https://open.spotify.com/track/4",
            "release_date": "2023-07-15"
        },
        {
            "id": "track5",
            "name": "Kahani Suno",
            "album_id": "album5",
            "album_name": "Kahaani 2",
            "popularity": 78,
            "external_spotify_url": "https://open.spotify.com/track/5", 
            "release_date": "2023-05-20"
        }
    ]
    
    # Sample artists
    sample_artists = [
        {
            "id": "artist1",
            "name": "Arijit Singh",
            "popularity": 98,
            "followers": 12500000,
            "external_spotify_url": "https://open.spotify.com/artist/1"
        },
        {
            "id": "artist2",
            "name": "Shreya Ghoshal", 
            "popularity": 95,
            "followers": 8900000,
            "external_spotify_url": "https://open.spotify.com/artist/2"
        },
        {
            "id": "artist3",
            "name": "Raghav Chaitanya",
            "popularity": 82,
            "followers": 2300000,
            "external_spotify_url": "https://open.spotify.com/artist/3"
        },
        {
            "id": "artist4",
            "name": "Sachin-Jigar",
            "popularity": 89,
            "followers": 4200000,
            "external_spotify_url": "https://open.spotify.com/artist/4"
        }
    ]
    
    # Connect to database
    conn = sqlite3.connect('india_music_insights.db')
    cursor = conn.cursor()
    
    try:
        # Insert artists
        for artist in sample_artists:
            cursor.execute("""
                INSERT OR REPLACE INTO artists 
                (spotify_id, name, popularity, followers, external_url, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                artist["id"],
                artist["name"], 
                artist["popularity"],
                artist["followers"],
                artist["external_spotify_url"],
                datetime.utcnow(),
                datetime.utcnow()
            ))
        
        # Insert tracks  
        for track in sample_tracks:
            cursor.execute("""
                INSERT OR REPLACE INTO tracks
                (spotify_id, name, album, popularity, external_url, 
                 album_release_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                track["id"],
                track["name"],
                track["album_name"], 
                track["popularity"],
                track["external_spotify_url"],
                track["release_date"],
                datetime.utcnow(),
                datetime.utcnow()
            ))
        
        # Link tracks to artists - need to get the actual database IDs first
        # First get the artist IDs from database
        artist_id_map = {}
        for artist in sample_artists:
            cursor.execute("SELECT id FROM artists WHERE spotify_id = ?", (artist["id"],))
            result = cursor.fetchone()
            if result:
                artist_id_map[artist["id"]] = result[0]
        
        # Get track IDs from database  
        track_id_map = {}
        for track in sample_tracks:
            cursor.execute("SELECT id FROM tracks WHERE spotify_id = ?", (track["id"],))
            result = cursor.fetchone() 
            if result:
                track_id_map[track["id"]] = result[0]
        
        track_artist_links = [
            ("track1", "artist1"),  # Kesariya - Arijit Singh
            ("track2", "artist1"),  # Apna Bana Le - Arijit Singh
            ("track3", "artist1"),  # Tum Kya Mile - Arijit Singh  
            ("track3", "artist2"),  # Tum Kya Mile - Shreya Ghoshal
            ("track4", "artist1"),  # Ve Kamleya - Arijit Singh
            ("track4", "artist2"),  # Ve Kamleya - Shreya Ghoshal
            ("track5", "artist3"),  # Kahani Suno - Raghav Chaitanya
        ]
        
        for track_spotify_id, artist_spotify_id in track_artist_links:
            if track_spotify_id in track_id_map and artist_spotify_id in artist_id_map:
                cursor.execute("""
                    INSERT OR REPLACE INTO track_artists (track_id, artist_id)
                    VALUES (?, ?)
                """, (track_id_map[track_spotify_id], artist_id_map[artist_spotify_id]))
        
        # Create a playlist
        cursor.execute("""
            INSERT OR REPLACE INTO playlists
            (spotify_id, name, description, external_url, market, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "playlist1",
            "Top 50 - India",
            "Most played songs in India", 
            "https://open.spotify.com/playlist/37i9dQZEVXbLZ52XmnySJg",
            "IN",
            datetime.utcnow(),
            datetime.utcnow()
        ))
        
        # Get the database ID of the playlist
        cursor.execute("SELECT id FROM playlists WHERE spotify_id = ?", ("playlist1",))
        playlist_db_id = cursor.fetchone()[0]
        
        # Create playlist snapshots
        snapshot_date = date.today()
        for i, track in enumerate(sample_tracks):
            track_db_id = track_id_map.get(track["id"])
            if track_db_id:
                cursor.execute("""
                    INSERT OR REPLACE INTO playlist_track_snapshots
                    (playlist_id, track_id, rank, snapshot_date, fetched_at, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    playlist_db_id,
                    track_db_id,
                    i + 1,
                    snapshot_date,
                    datetime.utcnow(),
                    datetime.utcnow(),
                    datetime.utcnow()
                ))
        
        conn.commit()
        print(f"✅ Successfully added {len(sample_tracks)} tracks and {len(sample_artists)} artists")
        print("🎵 Sample data loaded! Your dashboard should now show real data.")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_sample_data()
