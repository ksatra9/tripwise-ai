@echo off
echo ======================================================================
echo Starting TripWise AI - Personalized Travel Recommendation System
echo ======================================================================

echo [1/2] Launching FastAPI Backend on http://localhost:8000 ...
start "TripWise AI Backend" cmd /k "python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Launching Vite Frontend on http://localhost:5173 ...
cd frontend
start "TripWise AI Frontend" cmd /k "npm run dev"

echo ======================================================================
echo Both servers are starting!
echo Backend Swagger API: http://localhost:8000/docs
echo Frontend Web UI:    http://localhost:5173
echo ======================================================================
pause
