@echo off
REM Quick activation script untuk venv
REM Usage: activate.bat

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo ================================
echo Virtual environment activated!
echo ================================
echo.
echo To install dependencies:
echo   pip install -r requirements.txt
echo.
echo To run scraper:
echo   python scrape_tanahkita.py
echo.
