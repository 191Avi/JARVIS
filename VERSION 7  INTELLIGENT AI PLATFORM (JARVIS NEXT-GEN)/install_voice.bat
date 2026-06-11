@echo off
title JARVIS v7 - Voice Setup
echo ========================================
echo   JARVIS v7 - Installing Voice Support
echo   (sounddevice method - Python 3.14 safe)
echo ========================================
echo.

pip install sounddevice scipy SpeechRecognition pyttsx3

echo.
echo Verifying...
python -c "import sounddevice; print('sounddevice OK'); import scipy; print('scipy OK'); import speech_recognition; print('SpeechRecognition OK'); import pyttsx3; print('pyttsx3 OK')"

echo.
echo ========================================
echo   Done! Run run_client.bat to start.
echo ========================================
pause
