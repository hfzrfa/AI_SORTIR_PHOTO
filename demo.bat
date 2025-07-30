@echo off
echo ========================================
echo      AI Photo Sorter - DEMO TEST
echo ========================================
echo.

echo [INFO] Membuat gambar demo...
python create_demo.py

echo.
echo [INFO] Memulai aplikasi Photo Sorter...
echo [TIPS] Gunakan folder 'demo_photos' sebagai sumber
echo [TIPS] Buat folder baru sebagai tujuan (misal: 'hasil_sortir')
echo.

python photo_sorter_opencv.py

echo.
echo [INFO] Demo selesai!
pause
