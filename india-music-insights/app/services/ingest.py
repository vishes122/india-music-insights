"""
Ingestion service for fetching and storing Spotify data
"""

import asyncio
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import Artist, Track, Playlist, PlaylistTrackSnapshot, track_artists
from ..clients.spotify import SpotifyClient, SpotifyAPIError
from ..config import settings, get_market_config
from ..utils.time import today_in_timezone, now_in_timezone
from ..utils.logging import get_request_logger

logger = get_request_logger()


class IngestionService:
    """
    Service for ingesting Spotify playlist data into the database
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def ingest_top_playlist(
        self, 
        market: str = "IN",
        playlist_id: Optional[str] = None,
        snapshot_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Ingest top playlist for a market
        
        Args:
            market: Market code (e.g., "IN", "US")
            playlist_id: Override playlist ID (uses config if None)
            snapshot_date: Override snapshot date (uses today if None)
            
        Returns:
            dict: Ingestion results
        """
        start_time = datetime.utcnow()
        
        # Get market configuration
        market_config = get_market_config(market)
        playlist_id = playlist_id or market_config["playlist_id"]
        snapshot_date = snapshot_date or today_in_timezone(market_config["timezone"])
        
        logger.info(
            "Starting playlist ingestion",
            market=market,
            playlist_id=playlist_id,
            snapshot_date=snapshot_date.isoformat()
        )
        
        try:
            async with SpotifyClient() as spotify_client:
                # Fetch playlist tracks
                playlist_data = await spotify_client.get_playlist_tracks(
                    playlist_id=playlist_id,
                    market=market,
                    limit=50
                )
                
                # Process the data
                results = await self._process_playlist_data(
                    playlist_data=playlist_data,
                    market=market,
                    playlist_id=playlist_id,
                    snapshot_date=snapshot_date
                )
                
                duration = (datetime.utcnow() - start_time).total_seconds()
                
                logger.info(
                    "Playlist ingestion completed",
                    market=market,
                    **results,
                    duration_seconds=duration
                )
                
                return {
                    "success": True,
                    "market": market,
                    "snapshot_date": snapshot_date,
                    "duration_seconds": duration,
                    **results
                }
                
        except SpotifyAPIError as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.error(
                "Spotify API error during ingestion",
                market=market,
                error=str(e),
                status_code=e.status_code,
                duration_seconds=duration
            )
            raise
            
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.error(
                "Unexpected error during ingestion",
                market=market,
                error=str(e),
                duration_seconds=duration
            )
            raise
    
    async def _process_playlist_data(
        self,
        playlist_data: Dict[str, Any],
        market: str,
        playlist_id: str,
        snapshot_date: date
    ) -> Dict[str, Any]:
        """
        Process playlist data and store in database
        
        Args:
            playlist_data: Playlist data from Spotify API
            market: Market code
            playlist_id: Playlist ID
            snapshot_date: Snapshot date
            
        Returns:
            dict: Processing results
        """
        tracks_processed = 0
        artists_processed = 0
        
        # Ensure playlist exists
        playlist = await self._ensure_playlist(playlist_id, market)
        
        # Process each track
        track_items = playlist_data.get("items", [])
        
        for rank, item in enumerate(track_items, 1):
            track_data = item.get("track")
            if not track_data:
                continue
            
            try:
                # Upsert track and artists
                track, new_artists = await self._upsert_track(track_data)
                tracks_processed += 1
                artists_processed += len(new_artists)
                
                # Create or update snapshot entry
                await self._upsert_playlist_snapshot(
                    playlist=playlist,
                    track=track,
                    rank=rank,
                    snapshot_date=snapshot_date,
                    added_at=self._parse_spotify_date(item.get("added_at"))
                )
                
            except Exception as e:
                logger.error(
                    "Error processing track",
                    track_id=track_data.get("id"),
                    track_name=track_data.get("name"),
                    error=str(e)
                )
                continue
        
        # Commit changes
        self.db.commit()
        
        return {
            "tracks_processed": tracks_processed,
            "artists_processed": artists_processed,
            "message": f"Successfully processed {tracks_processed} tracks"
        }
    
    async def _ensure_playlist(self, playlist_id: str, market: str) -> Playlist:
        """
        Ensure playlist exists in database
        
        Args:
            playlist_id: Spotify playlist ID
            market: Market code
            
        Returns:
            Playlist: Database playlist record
        """
        playlist = self.db.query(Playlist).filter(
            Playlist.spotify_id == playlist_id
        ).first()
        
        if not playlist:
            # Create new playlist record
            playlist = Playlist(
                spotify_id=playlist_id,
                name=f"Top 50 - {market}",  # Will be updated with real data later
                market=market,
                description="Top 50 tracks playlist"
            )
            self.db.add(playlist)
            self.db.flush()  # Get ID
        
        return playlist
    
    async def _upsert_track(self, track_data: Dict[str, Any]) -> Tuple[Track, List[Artist]]:
        """
        Upsert track and its artists
        
        Args:
            track_data: Track data from Spotify API
            
        Returns:
            tuple: (Track instance, list of new Artist instances)
        """
        spotify_id = track_data["id"]
        
        # Check if track exists
        track = self.db.query(Track).filter(Track.spotify_id == spotify_id).first()
        
        if track:
            # Update existing track
            self._update_track_from_data(track, track_data)
        else:
            # Create new track
            track = self._create_track_from_data(track_data)
            self.db.add(track)
            self.db.flush()  # Get ID
        
        # Process artists
        new_artists = []
        track_artist_ids = []
        
        for artist_data in track_data.get("artists", []):
            artist, is_new = await self._upsert_artist(artist_data)
            if is_new:
                new_artists.append(artist)
            track_artist_ids.append(artist.id)
        
        # Update track-artist relationships
        # Clear existing relationships
        self.db.execute(
            track_artists.delete().where(track_artists.c.track_id == track.id)
        )
        
        # Add new relationships
        for artist_id in track_artist_ids:
            self.db.execute(
                track_artists.insert().values(track_id=track.id, artist_id=artist_id)
            )
        
        return track, new_artists
    
    async def _upsert_artist(self, artist_data: Dict[str, Any]) -> Tuple[Artist, bool]:
        """
        Upsert artist
        
        Args:
            artist_data: Artist data from Spotify API
            
        Returns:
            tuple: (Artist instance, is_new boolean)
        """
        spotify_id = artist_data["id"]
        
        # Check if artist exists
        artist = self.db.query(Artist).filter(Artist.spotify_id == spotify_id).first()
        
        if artist:
            # Update existing artist
            self._update_artist_from_data(artist, artist_data)
            return artist, False
        else:
            # Create new artist
            artist = self._create_artist_from_data(artist_data)
            self.db.add(artist)
            self.db.flush()  # Get ID
            return artist, True
    
    async def _upsert_playlist_snapshot(
        self,
        playlist: Playlist,
        track: Track,
        rank: int,
        snapshot_date: date,
        added_at: Optional[datetime] = None
    ) -> PlaylistTrackSnapshot:
        """
        Upsert playlist track snapshot
        
        Args:
            playlist: Playlist instance
            track: Track instance
            rank: Track rank in playlist
            snapshot_date: Snapshot date
            added_at: When track was added to playlist
            
        Returns:
            PlaylistTrackSnapshot: Snapshot instance
        """
        # Check if snapshot exists
        snapshot = self.db.query(PlaylistTrackSnapshot).filter(
            and_(
                PlaylistTrackSnapshot.playlist_id == playlist.id,
                PlaylistTrackSnapshot.track_id == track.id,
                PlaylistTrackSnapshot.snapshot_date == snapshot_date
            )
        ).first()
        
        if snapshot:
            # Update existing snapshot
            snapshot.rank = rank
            snapshot.added_at = added_at or snapshot.added_at
        else:
            # Create new snapshot
            snapshot = PlaylistTrackSnapshot(
                playlist_id=playlist.id,
                track_id=track.id,
                rank=rank,
                snapshot_date=snapshot_date,
                added_at=added_at,
                fetched_at=datetime.utcnow()
            )
            self.db.add(snapshot)
        
        return snapshot
    
    def _create_track_from_data(self, track_data: Dict[str, Any]) -> Track:
        """Create Track instance from Spotify data"""
        album_data = track_data.get("album", {})
        
        return Track(
            spotify_id=track_data["id"],
            name=track_data["name"],
            album=album_data.get("name"),
            album_release_date=album_data.get("release_date"),
            duration_ms=track_data.get("duration_ms"),
            explicit=track_data.get("explicit", False),
            popularity=track_data.get("popularity", 0),
            preview_url=track_data.get("preview_url"),
            external_url=track_data.get("external_urls", {}).get("spotify")
        )
    
    def _update_track_from_data(self, track: Track, track_data: Dict[str, Any]):
        """Update Track instance with fresh Spotify data"""
        album_data = track_data.get("album", {})
        
        track.name = track_data["name"]
        track.album = album_data.get("name") or track.album
        track.album_release_date = album_data.get("release_date") or track.album_release_date
        track.duration_ms = track_data.get("duration_ms") or track.duration_ms
        track.explicit = track_data.get("explicit", track.explicit)
        track.popularity = track_data.get("popularity", track.popularity)
        track.preview_url = track_data.get("preview_url") or track.preview_url
        track.external_url = track_data.get("external_urls", {}).get("spotify") or track.external_url
    
    def _create_artist_from_data(self, artist_data: Dict[str, Any]) -> Artist:
        """Create Artist instance from Spotify data"""
        return Artist(
            spotify_id=artist_data["id"],
            name=artist_data["name"],
            popularity=artist_data.get("popularity", 0),
            followers=artist_data.get("followers", {}).get("total", 0),
            genres_json=artist_data.get("genres", []),
            external_url=artist_data.get("external_urls", {}).get("spotify")
        )
    
    def _update_artist_from_data(self, artist: Artist, artist_data: Dict[str, Any]):
        """Update Artist instance with fresh Spotify data"""
        artist.name = artist_data["name"]
        artist.popularity = artist_data.get("popularity", artist.popularity)
        artist.followers = artist_data.get("followers", {}).get("total", artist.followers)
        artist.genres_json = artist_data.get("genres", artist.genres_json)
        artist.external_url = artist_data.get("external_urls", {}).get("spotify") or artist.external_url
    
    def _parse_spotify_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse Spotify ISO date string"""
        if not date_str:
            return None
        
        try:
            # Spotify uses ISO format: "2023-12-25T10:30:00Z"
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
