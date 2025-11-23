@echo off
color 0A
cls

echo.
echo ========================================
echo    TalkToBank Digital Platform
echo ========================================
echo.
echo Starting application...
echo.

REM Start backend
echo [1/2] Starting Backend Server...
cd /d "%~dp0backend"
start "TalkToBank Backend" /MIN python app.py
timeout /t 3 /nobreak >nul
echo      Backend running on http://localhost:5001
echo.

REM Open enhanced frontend
echo [2/2] Launching Web Interface...
start "" "%~dp0frontend\index.html"
timeout /t 2 /nobreak >nul
echo.

echo ========================================
echo    READY FOR DEMO!
echo ========================================
echo.
echo UNIQUE FEATURES TO SHOWCASE:
echo  [1] AI Financial Advisor
echo  [2] Document OCR Upload
echo  [3] Financial Health Score
echo  [4] Predictive Analytics
echo  [5] Multi-Modal Input
echo  [6] Voice Assistant
echo.
echo QUICK DEMO COMMANDS:
echo  - "Check my balance"
echo  - "Transfer 1000 to John"
echo  - Click "Upload Document"
echo  - Click "Get AI Advice"
echo  - Click "Check Health Score"
echo.
echo Backend: http://localhost:5001
echo Frontend: Opened in browser
echo.
echo Press Ctrl+C to stop servers
pause