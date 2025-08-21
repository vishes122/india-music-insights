#!/usr/bin/env python3
"""
Railway deployment entry point for India Music Insights
This file helps Railway detect the project as a Python application
"""

import sys
import os
import subprocess

def main():
    """Main entry point that starts the FastAPI application"""
    # Change to the backend directory
    os.chdir('india-music-insights')
    
    # Start the FastAPI application
    subprocess.run([
        sys.executable, '-m', 'uvicorn', 
        'app.main:app', 
        '--host', '0.0.0.0', 
        '--port', os.environ.get('PORT', '8000')
    ])

if __name__ == "__main__":
    main()
