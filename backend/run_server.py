#!/usr/bin/env python3
"""
Simple server startup script that ensures proper working directory
"""
import os
import sys
import subprocess

# Change to backend directory
backend_dir = r"C:\Users\SKuppili1_GPS\immigration-law-dashboard\backend"
os.chdir(backend_dir)

# Add backend directory to Python path
sys.path.insert(0, backend_dir)

# Verify we can import the app
try:
    import app.main
    print("✅ App module imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import app module: {e}")
    sys.exit(1)

# Start uvicorn server
print(f"Starting FastAPI server from: {os.getcwd()}")
subprocess.run([
    sys.executable, "-m", "uvicorn", 
    "app.main:app", 
    "--reload", 
    "--host", "127.0.0.1", 
    "--port", "8000"
])
