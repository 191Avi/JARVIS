@echo off
title JARVIS v7 Voice Client
echo ========================================
echo   JARVIS v7 — Voice Client
echo   Make sure run_backend.bat is running!
echo ========================================
echo.
cd /d "%~dp0client"
python client.py
pause
