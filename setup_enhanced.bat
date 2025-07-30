@echo off
title HFZRFA AI Photo Sorter - Professional Setup
color 0A

echo ================================================
echo     HFZRFA AI Photo Sorter - Setup
echo     Professional Photo Organization System
echo ================================================
echo.
echo [INFO] Installing enhanced AI dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INSTALL] Upgrading pip...
python -m pip install --upgrade pip

echo [INSTALL] Installing core requirements...
python -m pip install opencv-python>=4.8.0
python -m pip install pillow>=9.0.0
python -m pip install numpy>=1.21.0

echo [INSTALL] Installing enhanced AI features...
python -m pip install scikit-image>=0.19.0

echo.
echo [SUCCESS] HFZRFA AI Photo Sorter setup completed!
echo [INFO] You can now run the application using:
echo        - python photo_sorter_advanced.py
echo        - Or double-click run.bat
echo.
echo Powered by HFZRFA Advanced AI Technology
pause
