@echo off

cd /d "%~dp0"

echo ==========================================
echo       STA Contest Monitor
echo ==========================================
echo.

call ".venv\Scripts\activate.bat"

python main.py

echo.
echo ==========================================
echo          Monitor Finished
echo ==========================================
echo.

pause