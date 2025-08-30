@echo off
cd /d "C:\Users\SKuppili1_GPS\immigration-law-dashboard\backend"
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
