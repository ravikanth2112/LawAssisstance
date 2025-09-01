"""
Simple server runner
"""

import sys
from pathlib import Path

# Add the app directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Immigration Law Dashboard API Server...")
    print("📍 Server will be available at: http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("🔄 ReDoc Documentation: http://127.0.0.1:8000/redoc")
    print("-" * 50)
    
    uvicorn.run(
        "app.main_simple:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["app"]
    )
