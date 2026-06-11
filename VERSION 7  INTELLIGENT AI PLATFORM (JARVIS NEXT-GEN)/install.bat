@echo off
title JARVIS v7 Installer
echo ========================================
echo   JARVIS v7 — Installing dependencies
echo ========================================
echo.
cd /d "%~dp0"
pip install -r requirements.txt
echo.
echo ========================================
echo   Done! Now:
echo   1. Copy .env.example to .env and add YOUR OWN OpenAI key
echo   2. Run run_backend.bat
echo   3. Run run_client.bat  OR  open http://localhost:8000/ui
echo ========================================
pause
