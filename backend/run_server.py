#!/usr/bin/env python3
"""
Immigration Law Dashboard API Server
Run this script to start the FastAPI development server
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the app directory to Python path
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
sys.path.insert(0, str(current_dir))

def main():
    """Start the FastAPI server"""
    
    print("🚀 Starting Immigration Law Dashboard API Server...")
    print("📍 Server will be available at: http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("🔄 ReDoc Documentation: http://127.0.0.1:8000/redoc")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            reload_dirs=[str(app_dir)],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
