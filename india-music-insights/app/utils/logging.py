"""
Structured logging configuration for India Music Insights
"""

import logging
import sys
from typing import Any, Dict
import structlog
from structlog import get_logger

from ..config import settings


def configure_logging():
    """
    Configure structured logging with appropriate settings
    """
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper())
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.dev.ConsoleRenderer() if settings.is_development else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_request_logger(request_id: str = None) -> Any:
    """
    Get logger with request context
    
    Args:
        request_id: Request ID for tracking
        
    Returns:
        Structured logger with request context
    """
    logger = get_logger()
    if request_id:
        logger = logger.bind(request_id=request_id)
    return logger


def log_api_call(
    logger: Any,
    method: str,
    url: str,
    status_code: int = None,
    duration: float = None,
    **kwargs
):
    """
    Log API call with structured data
    
    Args:
        logger: Structured logger instance
        method: HTTP method
        url: API URL
        status_code: HTTP status code
        duration: Request duration in seconds
        **kwargs: Additional context
    """
    log_data = {
        "event": "api_call",
        "method": method,
        "url": url,
        **kwargs
    }
    
    if status_code is not None:
        log_data["status_code"] = status_code
    
    if duration is not None:
        log_data["duration_ms"] = round(duration * 1000, 2)
    
    if status_code and status_code >= 400:
        logger.error("API call failed", **log_data)
    else:
        logger.info("API call completed", **log_data)


def log_database_operation(
    logger: Any,
    operation: str,
    table: str = None,
    duration: float = None,
    rows_affected: int = None,
    **kwargs
):
    """
    Log database operation with structured data
    
    Args:
        logger: Structured logger instance
        operation: Database operation (SELECT, INSERT, etc.)
        table: Table name
        duration: Query duration in seconds
        rows_affected: Number of rows affected
        **kwargs: Additional context
    """
    log_data = {
        "event": "database_operation",
        "operation": operation,
        **kwargs
    }
    
    if table:
        log_data["table"] = table
    
    if duration is not None:
        log_data["duration_ms"] = round(duration * 1000, 2)
    
    if rows_affected is not None:
        log_data["rows_affected"] = rows_affected
    
    logger.info("Database operation completed", **log_data)


class RequestContextMiddleware:
    """
    Middleware to add request context to logs
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Generate request ID
            import uuid
            request_id = str(uuid.uuid4())[:8]
            
            # Add to structlog context
            structlog.contextvars.clear_contextvars()
            structlog.contextvars.bind_contextvars(
                request_id=request_id,
                path=scope.get("path"),
                method=scope.get("method")
            )
        
        await self.app(scope, receive, send)
