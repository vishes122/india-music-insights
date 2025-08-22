"""
Main FastAPI application for India Music Insights
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .config import settings
from .db import init_db, close_db
from .utils.logging import configure_logging, RequestContextMiddleware
from .routers import health, charts
from . import models  # Import models to ensure they're registered with Base


# Configure logging
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    """
    # Startup
    print(f"🚀 Starting {settings.app_name} v{settings.version}")
    
    # Initialize database
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise
    
    # Start scheduler if enabled
    if settings.enable_scheduler:
        try:
            from .jobs.scheduler import scheduler
            scheduler.start()
            print("✅ Job scheduler started")
        except Exception as e:
            print(f"⚠️ Scheduler failed to start: {e}")
    
    print(f"🎵 {settings.app_name} is ready!")
    print(f"📚 API Documentation: http://localhost:{settings.port}/docs")
    print(f"🔍 Health Check: http://localhost:{settings.port}/v1/health")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    
    # Stop scheduler
    if settings.enable_scheduler:
        try:
            from .jobs.scheduler import scheduler
            scheduler.shutdown()
            print("✅ Scheduler stopped")
        except:
            pass
    
    # Close database connections
    try:
        close_db()
        print("✅ Database connections closed")
    except:
        pass
    
    print("👋 Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="A comprehensive API for music insights and analytics from Spotify data",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    debug=settings.debug
)

# Add middleware
app.add_middleware(RequestContextMiddleware)

# CORS Configuration - Allow specific origins
allowed_origins = [
    "https://india-music-insights.vercel.app",  # Production Vercel domain
    "http://localhost:3000",                    # Local React dev server
    "http://localhost:5173",                    # Local Vite dev server
    "http://localhost:8080",                    # Alternative local server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080"
]

# Add any additional origins from environment
if settings.cors_origins_list:
    for origin in settings.cors_origins_list:
        if origin not in allowed_origins:
            allowed_origins.append(origin)

print(f"🌐 CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
    )

# Include routers
app.include_router(health.router)
app.include_router(charts.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler
    """
    from .utils.logging import get_request_logger
    
    logger = get_request_logger()
    logger.error(
        "Unhandled exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        error_type=type(exc).__name__
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "internal_server_error",
            "message": "An unexpected error occurred"
        }
    )


@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": "healthy",
        "documentation": "/docs",
        "health_check": "/v1/health",
        "markets": settings.markets
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development,
        log_level=settings.log_level.lower()
    )
