@echo off
title AI Photo Sorter - Launcher
color 0A

:menu
cls
echo ================================================
echo         🚀 AI PHOTO SORTER LAUNCHER 🚀
echo ================================================
echo.
echo Pilih versi yang ingin dijalankan:
echo.
echo [1] 🌟 AUTO CLUSTERING (RECOMMENDED)
echo     - Otomatis kelompokkan orang yang sama
echo     - Hasil: Person_01, Person_02, dst
echo     - Mudah install (OpenCV only)
echo.
echo [2] 📊 SORTIR BERDASARKAN JUMLAH WAJAH
echo     - Kategori: 1 wajah, 2 wajah, dst
echo     - Versi paling ringan
echo     - Hasil cepat
echo.
echo [3] 🎯 ADVANCED RECOGNITION
echo     - Database wajah dikenal + Auto Clustering
echo     - Paling canggih dan akurat
echo     - Butuh instalasi face_recognition
echo.
echo [4] 📖 BUKA DOKUMENTASI
echo [5] 🔧 CEK INSTALASI
echo [0] ❌ KELUAR
echo.
echo ================================================

set /p choice="Masukkan pilihan (0-5): "

if "%choice%"=="1" goto auto_clustering
if "%choice%"=="2" goto opencv_simple
if "%choice%"=="3" goto advanced_recognition
if "%choice%"=="4" goto documentation
if "%choice%"=="5" goto check_install
if "%choice%"=="0" goto exit

echo [ERROR] Pilihan tidak valid!
timeout /t 2 /nobreak >nul
goto menu

:auto_clustering
cls
echo ================================================
echo        🌟 MENJALANKAN AUTO CLUSTERING
echo ================================================
echo.
python photo_sorter_advanced.py
if %errorlevel% neq 0 (
    echo [ERROR] Gagal menjalankan auto clustering!
    pause
)
goto menu

:opencv_simple
cls
echo ================================================
echo       📊 MENJALANKAN OPENCV SIMPLE
echo ================================================
echo.
python photo_sorter_opencv.py
if %errorlevel% neq 0 (
    echo [ERROR] Gagal menjalankan OpenCV simple!
    pause
)
goto menu

:advanced_recognition
cls
echo ================================================
echo      🎯 MENJALANKAN ADVANCED RECOGNITION
echo ================================================
echo.
python photo_sorter_gui.py
if %errorlevel% neq 0 (
    echo [ERROR] Gagal menjalankan advanced recognition!
    echo [INFO] Pastikan face_recognition sudah terinstall.
    pause
)
goto menu

:documentation
cls
echo ================================================
echo            📖 MEMBUKA DOKUMENTASI
echo ================================================
echo.
if exist "README.md" (
    start notepad "README.md"
    echo [INFO] README.md dibuka di Notepad
) else (
    echo [ERROR] README.md tidak ditemukan!
)
echo.
if exist "QUICK_START.md" (
    start notepad "QUICK_START.md"
    echo [INFO] QUICK_START.md dibuka di Notepad
) else (
    echo [ERROR] QUICK_START.md tidak ditemukan!
)
echo.
pause
goto menu

:check_install
cls
echo ================================================
echo            🔧 CHECKING INSTALLATION
echo ================================================
echo.

echo [CHECK] Python installation...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak terinstall!
    echo Download dari: https://www.python.org/downloads/
    goto check_done
)

echo.
echo [CHECK] Required packages...

echo Checking OpenCV...
python -c "import cv2; print('OpenCV:', cv2.__version__)"
if %errorlevel% neq 0 (
    echo [ERROR] OpenCV tidak terinstall!
    echo Run: pip install opencv-python
)

echo Checking PIL...
python -c "import PIL; print('PIL: OK')"
if %errorlevel% neq 0 (
    echo [ERROR] PIL tidak terinstall!
    echo Run: pip install pillow
)

echo Checking numpy...
python -c "import numpy; print('NumPy:', numpy.__version__)"
if %errorlevel% neq 0 (
    echo [ERROR] NumPy tidak terinstall!
    echo Run: pip install numpy
)

echo.
echo [CHECK] Optional packages...

echo Checking face_recognition...
python -c "import face_recognition; print('face_recognition: OK')"
if %errorlevel% neq 0 (
    echo [WARNING] face_recognition tidak terinstall!
    echo [INFO] Hanya dibutuhkan untuk versi Advanced Recognition
    echo [INFO] Install: pip install face_recognition
)

:check_done
echo.
echo ================================================
pause
goto menu

:exit
cls
echo ================================================
echo       Terima kasih telah menggunakan
echo           🚀 AI Photo Sorter 🚀
echo ================================================
echo.
timeout /t 2 /nobreak >nul
exit /b 0
