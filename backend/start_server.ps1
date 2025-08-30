# PowerShell script to start the FastAPI server
Set-Location "C:\Users\SKuppili1_GPS\immigration-law-dashboard\backend"
& ".\venv\Scripts\Activate.ps1"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
