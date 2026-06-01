@echo off
title JARVIS v6 - Backend Server
color 0B
echo ========================================
echo   JARVIS v6 - Production Backend
echo   http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo ========================================
echo.

cd /d "%~dp0backend"
C:\python314\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo.
echo Backend stopped.
pause
