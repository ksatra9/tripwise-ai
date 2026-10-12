@echo off
echo ======================================================================
echo Starting TripWise AI FastAPI Backend on http://localhost:8000 ...
echo ======================================================================
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
