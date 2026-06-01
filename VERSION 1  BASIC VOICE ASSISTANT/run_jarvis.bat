@echo off
title JARVIS - Final Version (V1 + V2 + V3 Merged)
color 0A
echo ========================================
echo     JARVIS - FINAL MERGED VERSION
echo     (V1 + V2 + V3 combined)
echo ========================================
echo.
echo  Say "Hey Jarvis" then your command:
echo   - "what time is it"
echo   - "what is the date"
echo   - "open youtube"
echo   - "open google"
echo   - "open notepad"
echo   - "search wikipedia [topic]"
echo   - "take a screenshot"
echo   - "remember [something]"
echo   - "what do you remember"
echo   - "stop" or "exit"
echo.
echo Starting JARVIS... please wait...
echo.

set PYTHONUNBUFFERED=1

cd "C:\Users\ASUS\Desktop\JARVIS\VERSION 1 JARVIS (VOICE ASSISTANT)" && C:\python314\python.exe .\jarvis_final.py

echo.
echo JARVIS has stopped.
pause
