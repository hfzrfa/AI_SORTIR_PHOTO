@echo off
echo ========================================
echo  AI Photo Sorter - Setup Script
echo ========================================
echo.

echo [INFO] Memeriksa Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan!
    echo [INFO] Silakan install Python terlebih dahulu dari https://python.org
    pause
    exit /b 1
)

echo [INFO] Python ditemukan!
echo.

echo [INFO] Menginstall dependencies (versi mudah)...
echo.

echo [INFO] Installing opencv-python...
pip install opencv-python

echo [INFO] Installing Pillow...
pip install Pillow

echo [INFO] Installing numpy...
pip install numpy

echo.
echo [INFO] Memeriksa instalasi...
python -c "import cv2, PIL, numpy; print('[SUCCESS] Library utama berhasil diinstall!')" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Ada masalah dengan instalasi. Mencoba install dengan requirements.txt...
    pip install -r requirements.txt
)

echo.
echo ========================================
echo  Setup Selesai!
echo ========================================
echo.
echo Untuk menjalankan aplikasi:
echo.
echo [RECOMMENDED] Versi mudah (OpenCV):
echo   python photo_sorter_opencv.py
echo.
echo [ADVANCED] Versi canggih (Face Recognition):
echo   python photo_sorter_gui.py
echo   (Memerlukan instalasi tambahan: cmake, dlib, face-recognition)
echo.
pause
