@echo off
echo Starting Flask Chatbot Server...
echo.
cd /d "%~dp0src"
..\venv\Scripts\python.exe app_flask.py
pause
