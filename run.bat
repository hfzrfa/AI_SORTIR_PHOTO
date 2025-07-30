@echo off
title AI Photo Sorter

echo ========================================
echo       AI Photo Sorter v2.0
echo    Auto Clustering & Face Detection
echo ========================================
echo.

echo [INFO] Memulai aplikasi dengan Auto Clustering...
python photo_sorter_advanced.py

if %errorlevel% neq 0 (
    echo.
    echo [INFO] Mencoba versi OpenCV sederhana...
    python photo_sorter_opencv.py
)

echo.
echo [INFO] Aplikasi telah ditutup.
pause
