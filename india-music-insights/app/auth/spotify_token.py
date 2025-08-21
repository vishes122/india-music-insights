"""
Spotify token management using Client Credentials flow
"""

import base64
import time
from datetime import datetime, timedelta
from typing import Optional
import httpx
import logging

from ..config import settings

logger = logging.getLogger(__name__)


class SpotifyTokenManager:
    """
    Manages Spotify access tokens using Client Credentials flow
    Includes automatic token refresh and caching with 60s buffer
    """
    
    def __init__(self):
        self.access_token: Optional[str] = None
        self.expires_at: Optional[datetime] = None
        self.token_type: str = "Bearer"
        
    async def get_access_token(self) -> str:
        """
        Get valid access token, refreshing if necessary
        
        Returns:
            str: Valid access token
            
        Raises:
            httpx.HTTPError: If token request fails
        """
        # Return cached token if still valid
        if self.access_token and self.expires_at and datetime.now() < self.expires_at:
            return self.access_token
        
        # Request new token
        await self._refresh_token()
        return self.access_token
    
    async def _refresh_token(self) -> None:
        """
        Request new access token from Spotify
        """
        logger.info("Requesting new Spotify access token...")
        
        # Prepare credentials
        auth_string = f"{settings.spotify_client_id}:{settings.spotify_client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        
        # Make token request
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, data=data)
                response.raise_for_status()
                
                token_data = response.json()
                self.access_token = token_data['access_token']
                expires_in = token_data['expires_in']  # seconds
                
                # Set expiration with 60 second buffer
                self.expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
                
                logger.info(f"✅ Access token obtained, expires at: {self.expires_at}")
                
            except httpx.HTTPError as e:
                logger.error(f"Failed to get Spotify access token: {e}")
                raise
            except KeyError as e:
                logger.error(f"Invalid token response format: {e}")
                raise
    
    def get_auth_header(self) -> dict:
        """
        Get authorization header for API requests
        
        Returns:
            dict: Authorization header
        """
        if not self.access_token:
            raise ValueError("No access token available")
        
        return {"Authorization": f"{self.token_type} {self.access_token}"}
    
    def is_token_valid(self) -> bool:
        """
        Check if current token is valid
        
        Returns:
            bool: True if token is valid and not expired
        """
        return (
            self.access_token is not None and
            self.expires_at is not None and
            datetime.now() < self.expires_at
        )


# Global token manager instance
token_manager = SpotifyTokenManager()
