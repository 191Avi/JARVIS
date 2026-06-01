@echo off
title JARVIS v6 - Voice Client
color 0A
echo ========================================
echo   JARVIS v6 - Voice Client
echo   Make sure run_backend.bat is running!
echo ========================================
echo.

cd /d "%~dp0client"
C:\python314\python.exe client.py

echo.
echo Client stopped.
pause
