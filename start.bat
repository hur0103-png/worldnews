@echo off
echo Starting World News Clipper Application...
echo.
cd backend
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup first.
    pause
    exit /b
)
call venv\Scripts\activate.bat
echo Starting FastAPI server with static frontend...
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
