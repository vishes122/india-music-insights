"""
Configuration management for India Music Insights API
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App Configuration
    app_name: str = "India Music Insights API"
    version: str = "1.0.0"
    env: str = Field(default="development", alias="ENV")
    debug: bool = Field(default=True)
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    
    # Spotify API Configuration
    spotify_client_id: str = Field(..., alias="SPOTIFY_CLIENT_ID")
    spotify_client_secret: str = Field(..., alias="SPOTIFY_CLIENT_SECRET")
    
    # Database Configuration
    database_url: str = Field(..., alias="DATABASE_URL")
    
    # Security
    admin_key: str = Field(..., alias="ADMIN_KEY")
    
    # Playlist Configuration
    india_top50_playlist_id: str = Field(
        default="37i9dQZEVXbLZ52XmnySJg", 
        alias="INDIA_TOP50_PLAYLIST_ID"
    )
    global_top50_playlist_id: str = Field(
        default="37i9dQZEVXbMDoHDwVN2tF",
        alias="GLOBAL_TOP50_PLAYLIST_ID"
    )
    
    # Markets to track
    markets_str: str = Field(default="IN,US,GB", alias="MARKETS")
    
    @property
    def markets(self) -> List[str]:
        """Parse markets from comma-separated string"""
        return [market.strip().upper() for market in self.markets_str.split(",")]
    
    # Cache Configuration
    redis_url: Optional[str] = Field(default=None, alias="REDIS_URL")
    cache_ttl: int = Field(default=300)  # 5 minutes
    
    # Timezone
    timezone: str = Field(default="Asia/Kolkata", alias="TIMEZONE")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=100)
    
    # Job Scheduling
    enable_scheduler: bool = Field(default=True)
    snapshot_hour: int = Field(default=0)  # 00:30 IST
    snapshot_minute: int = Field(default=30)
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    @property
    def is_production(self) -> bool:
        return self.env.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        return self.env.lower() == "development"
    
    def get_playlist_id_for_market(self, market: str) -> str:
        """Get playlist ID for specific market"""
        market_playlists = {
            "IN": self.india_top50_playlist_id,
            "US": self.global_top50_playlist_id,  # Can be customized
            "GB": self.global_top50_playlist_id,  # Can be customized
        }
        return market_playlists.get(market.upper(), self.global_top50_playlist_id)


# Global settings instance
settings = Settings()


# Market configuration
MARKET_CONFIG = {
    "IN": {
        "name": "India",
        "playlist_id": settings.india_top50_playlist_id,
        "timezone": "Asia/Kolkata",
        "currency": "INR"
    },
    "US": {
        "name": "United States",
        "playlist_id": settings.global_top50_playlist_id,
        "timezone": "America/New_York",
        "currency": "USD"
    },
    "GB": {
        "name": "United Kingdom",
        "playlist_id": settings.global_top50_playlist_id,
        "timezone": "Europe/London",
        "currency": "GBP"
    }
}


def get_market_config(market: str) -> dict:
    """Get configuration for a specific market"""
    return MARKET_CONFIG.get(market.upper(), MARKET_CONFIG["IN"])
