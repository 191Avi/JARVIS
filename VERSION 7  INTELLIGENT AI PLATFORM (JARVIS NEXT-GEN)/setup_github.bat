@echo off
title Push JARVIS to GitHub (clean)
cd /d "%~dp0"

echo ========================================
echo   Pushing JARVIS to GitHub with CLEAN history
echo ========================================
echo.

:: Safety: make sure no real .env gets committed
if exist .env (
  echo WARNING: a .env file exists here. It is gitignored and will be skipped.
  echo.
)

:: Start a brand-new history so no old leaked key can travel with it
if exist .git rmdir /s /q .git
git init
git add .
git commit -m "JARVIS v7 - Intelligent AI Platform"
git branch -M main

:: Point at your repo (replace if your repo URL differs)
git remote remove origin 2>nul
git remote add origin https://github.com/191Avi/JARVIS.git

echo.
echo Force-pushing clean history...
git push origin main --force

echo.
if %errorlevel% equ 0 (
  echo ========================================
  echo   SUCCESS!  https://github.com/191Avi/JARVIS
  echo ========================================
) else (
  echo Push failed - read the error above.
)
pause
