#!/usr/bin/env python3
"""
Debug entry point for Railway deployment
"""

import os
import sys
import traceback

print("=== RAILWAY DEPLOYMENT DEBUG ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")
print(f"PORT environment variable: {os.environ.get('PORT', 'Not set')}")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

try:
    # Add the backend directory to the Python path
    backend_dir = os.path.join(os.path.dirname(__file__), 'india-music-insights')
    print(f"Backend directory: {backend_dir}")
    print(f"Backend directory exists: {os.path.exists(backend_dir)}")
    
    if os.path.exists(backend_dir):
        print(f"Backend directory contents: {os.listdir(backend_dir)}")
    
    sys.path.insert(0, backend_dir)
    os.chdir(backend_dir)
    
    print(f"Changed to directory: {os.getcwd()}")
    print(f"Current directory contents: {os.listdir('.')}")
    
    # Try to import the app
    print("Attempting to import FastAPI app...")
    from app.main import app
    print("FastAPI app imported successfully!")
    
    # Start the server
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting uvicorn server on port {port}...")
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    print("Full traceback:")
    traceback.print_exc()
    sys.exit(1)
