#!/usr/bin/env python3
"""
Railway deployment entry point for India Music Insights
This file helps Railway detect the project as a Python application
"""

import sys
import os

def main():
    """Main entry point that starts the FastAPI application"""
    # Change to the backend directory
    backend_path = os.path.join(os.path.dirname(__file__), 'india-music-insights')
    os.chdir(backend_path)
    
    # Add the backend directory to Python path
    sys.path.insert(0, backend_path)
    
    # Get the port from environment variable
    port = os.environ.get('PORT', '8000')
    
    # Import and run uvicorn programmatically
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(port),
        log_level="info"
    )

if __name__ == "__main__":
    main()
