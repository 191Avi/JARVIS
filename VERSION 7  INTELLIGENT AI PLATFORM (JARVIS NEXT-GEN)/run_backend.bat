@echo off
title JARVIS v7 Backend
echo ========================================
echo   JARVIS v7 - Backend Server
echo   http://localhost:8000
echo   Web UI: http://localhost:8000/ui
echo ========================================
echo.
echo Reading API key from .env (see .env.example)
echo.
cd /d "%~dp0backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
