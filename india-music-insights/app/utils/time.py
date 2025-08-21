"""
Time and timezone utilities for India Music Insights
"""

from datetime import datetime, date, timezone
import pytz
from typing import Optional

from ..config import settings


def get_timezone(tz_name: str = None) -> pytz.BaseTzInfo:
    """
    Get timezone object
    
    Args:
        tz_name: Timezone name (defaults to configured timezone)
        
    Returns:
        pytz timezone object
    """
    tz_name = tz_name or settings.timezone
    return pytz.timezone(tz_name)


def now_in_timezone(tz_name: str = None) -> datetime:
    """
    Get current datetime in specified timezone
    
    Args:
        tz_name: Timezone name (defaults to configured timezone)
        
    Returns:
        datetime: Current time in specified timezone
    """
    tz = get_timezone(tz_name)
    return datetime.now(tz)


def today_in_timezone(tz_name: str = None) -> date:
    """
    Get current date in specified timezone
    
    Args:
        tz_name: Timezone name (defaults to configured timezone)
        
    Returns:
        date: Current date in specified timezone
    """
    return now_in_timezone(tz_name).date()


def utc_to_timezone(dt: datetime, tz_name: str = None) -> datetime:
    """
    Convert UTC datetime to specified timezone
    
    Args:
        dt: UTC datetime
        tz_name: Target timezone name
        
    Returns:
        datetime: Converted datetime
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    tz = get_timezone(tz_name)
    return dt.astimezone(tz)


def datetime_to_utc(dt: datetime) -> datetime:
    """
    Convert datetime to UTC
    
    Args:
        dt: Input datetime
        
    Returns:
        datetime: UTC datetime
    """
    if dt.tzinfo is None:
        # Assume it's in the configured timezone
        tz = get_timezone()
        dt = tz.localize(dt)
    
    return dt.astimezone(timezone.utc)


def parse_spotify_date(date_str: str) -> Optional[date]:
    """
    Parse Spotify date string (various formats)
    
    Args:
        date_str: Date string from Spotify API
        
    Returns:
        date: Parsed date or None if invalid
    """
    if not date_str:
        return None
    
    # Try different formats
    formats = [
        "%Y-%m-%d",  # 2023-12-25
        "%Y-%m",     # 2023-12
        "%Y"         # 2023
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    return None


def get_year_start_end(year: int, tz_name: str = None) -> tuple[datetime, datetime]:
    """
    Get start and end datetime for a year in specified timezone
    
    Args:
        year: Year
        tz_name: Timezone name
        
    Returns:
        tuple: (start_datetime, end_datetime) in UTC
    """
    tz = get_timezone(tz_name)
    
    start = tz.localize(datetime(year, 1, 1, 0, 0, 0))
    end = tz.localize(datetime(year + 1, 1, 1, 0, 0, 0))
    
    return datetime_to_utc(start), datetime_to_utc(end)


def format_duration(duration_ms: int) -> str:
    """
    Format duration from milliseconds to MM:SS
    
    Args:
        duration_ms: Duration in milliseconds
        
    Returns:
        str: Formatted duration (MM:SS)
    """
    if not duration_ms:
        return "0:00"
    
    seconds = duration_ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    
    return f"{minutes}:{seconds:02d}"
