"""
Spotify API client for making HTTP requests
"""

import asyncio
from typing import List, Dict, Optional, Any
import httpx
import logging

from ..auth.spotify_token import token_manager
from ..config import settings

logger = logging.getLogger(__name__)


class SpotifyAPIError(Exception):
    """Custom exception for Spotify API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class SpotifyClient:
    """
    Low-level Spotify API client for making authenticated HTTP requests
    """
    
    BASE_URL = "https://api.spotify.com/v1"
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.aclose()
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        retries: int = 3
    ) -> Dict[str, Any]:
        """
        Make authenticated request to Spotify API with retry logic
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            data: Request body data
            retries: Number of retry attempts
            
        Returns:
            dict: API response data
            
        Raises:
            SpotifyAPIError: If request fails after retries
        """
        if not self.session:
            raise ValueError("Client not initialized. Use async context manager.")

        # Ensure we only use relative endpoints to avoid double base URL
        if endpoint.startswith("http"):
            # If someone passed an absolute URL, extract just the path
            from urllib.parse import urlparse
            parsed = urlparse(endpoint)
            endpoint = parsed.path.lstrip('/')
        
        # Clean endpoint and construct full URL
        clean_endpoint = endpoint.lstrip('/')
        url = f"{self.BASE_URL}/{clean_endpoint}"
        
        for attempt in range(retries + 1):
            try:
                # Get fresh access token
                token = await token_manager.get_access_token()
                headers = {"Authorization": f"Bearer {token}"}
                
                # Make request
                logger.info(
                    "Spotify request",
                    extra={
                        "method": method,
                        "url": url,
                        "params": params,
                        "attempt": attempt + 1,
                        "retries": retries + 1,
                    },
                )
                response = await self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data
                )
                logger.info(
                    "Spotify response",
                    extra={
                        "method": method,
                        "url": url,
                        "status_code": response.status_code,
                    },
                )
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 1))
                    logger.warning(f"Rate limited. Retrying after {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                    continue
                
                # Handle unauthorized (token might be expired)
                if response.status_code == 401:
                    logger.warning("Token expired, refreshing...")
                    token_manager.access_token = None  # Force refresh
                    continue
                
                # Check for success
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                # Log a compact error snippet for diagnostics
                resp_text = None
                try:
                    resp_text = e.response.text
                except Exception:
                    resp_text = None

                snippet = (resp_text[:300] + "…") if resp_text and len(resp_text) > 300 else resp_text
                logger.error(
                    "Spotify HTTP error",
                    extra={
                        "url": e.request.url.__str__() if e.request else None,
                        "status_code": e.response.status_code if e.response else None,
                        "error_snippet": snippet,
                        "attempt": attempt + 1,
                        "retries": retries + 1,
                    },
                )

                if attempt == retries:
                    error_data = None
                    try:
                        error_data = e.response.json()
                    except Exception:
                        pass

                    raise SpotifyAPIError(
                        f"Spotify API error: {e.response.status_code} - {e.response.text}",
                        status_code=e.response.status_code,
                        response_data=error_data
                    )

                logger.warning(f"Request failed (attempt {attempt + 1}/{retries + 1}): {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except httpx.RequestError as e:
                if attempt == retries:
                    raise SpotifyAPIError(f"Network error: {str(e)}")
                    
                logger.warning(f"Network error (attempt {attempt + 1}/{retries + 1}): {e}")
                await asyncio.sleep(2 ** attempt)
        
        raise SpotifyAPIError("Max retries exceeded")
    
    async def get_playlist_tracks(self, playlist_id: str, limit: int = 50) -> Dict:
        """Get tracks from a playlist."""
        endpoint = f"playlists/{playlist_id}/tracks"
        params = {
            "market": "IN",
            "limit": limit,
            "fields": "items(track(id,name,artists(id,name),album(id,name,release_date),popularity,external_urls))"
        }
        return await self._make_request("GET", endpoint, params=params)
    
    async def search_tracks(self, query: str, year: int = None, year_range: str = None, 
                           limit: int = 50, offset: int = 0) -> Dict:
        """
        Search for tracks with optional year filtering.
        
        Args:
            query: Search query (artist, track name, etc.)
            year: Single year filter (e.g., 2020)
            year_range: Year range filter (e.g., "2018-2022")
            limit: Number of results (max 50)
            offset: Pagination offset
        """
        # Build the search query
        search_query = query
        
        # Add year filter if provided
        if year:
            search_query += f" year:{year}"
        elif year_range:
            search_query += f" year:{year_range}"
        
        # Add Indian context to search
        if "india" not in search_query.lower() and "bollywood" not in search_query.lower():
            search_query += " india OR bollywood OR hindi"
        
        params = {
            "q": search_query,
            "type": "track",
            "market": "IN",
            "limit": limit,
            "offset": offset
        }
        logger.info(
            "Built Spotify track search",
            extra={
                "q": search_query,
                "year": year,
                "year_range": year_range,
                "limit": limit,
                "offset": offset,
            },
        )
        return await self._make_request("GET", "search", params=params)
    
    async def search_artists(self, query: str, year: int = None, year_range: str = None,
                            limit: int = 50, offset: int = 0) -> Dict:
        """
        Search for artists with optional year filtering.
        """
        search_query = query
        
        if year:
            search_query += f" year:{year}"
        elif year_range:
            search_query += f" year:{year_range}"
        
        if "india" not in search_query.lower() and "bollywood" not in search_query.lower():
            search_query += " india OR bollywood OR hindi"
        
        params = {
            "q": search_query,
            "type": "artist",
            "market": "IN", 
            "limit": limit,
            "offset": offset
        }
        logger.info(
            "Built Spotify artist search",
            extra={
                "q": search_query,
                "year": year,
                "year_range": year_range,
                "limit": limit,
                "offset": offset,
            },
        )
        return await self._make_request("GET", "search", params=params)
    
    async def get_artist(self, artist_id: str) -> Dict[str, Any]:
        """
        Get artist details
        
        Args:
            artist_id: Spotify artist ID
            
        Returns:
            dict: Artist data
        """
        return await self._make_request("GET", f"artists/{artist_id}")
    
    async def get_artist_top_tracks(self, artist_id: str, market: str = "IN") -> Dict[str, Any]:
        """
        Get artist's top tracks
        
        Args:
            artist_id: Spotify artist ID
            market: Market code
            
        Returns:
            dict: Top tracks data
        """
        params = {"market": market}
        return await self._make_request("GET", f"artists/{artist_id}/top-tracks", params=params)
    
    async def search(
        self, 
        query: str, 
        search_type: str = "track",
        market: str = "IN",
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search Spotify catalog
        
        Args:
            query: Search query
            search_type: Type to search for (track, artist, album, playlist)
            market: Market code
            limit: Number of results
            offset: Offset for pagination
            
        Returns:
            dict: Search results
        """
        params = {
            "q": query,
            "type": search_type,
            "market": market,
            "limit": min(limit, 50),
            "offset": offset
        }
        
        return await self._make_request("GET", "search", params=params)
    
    async def get_audio_features(self, track_ids: List[str]) -> Dict[str, Any]:
        """
        Get audio features for multiple tracks
        
        Args:
            track_ids: List of Spotify track IDs (max 100)
            
        Returns:
            dict: Audio features data
        """
        if len(track_ids) > 100:
            raise ValueError("Maximum 100 track IDs allowed")
        
        params = {"ids": ",".join(track_ids)}
        return await self._make_request("GET", "audio-features", params=params)
