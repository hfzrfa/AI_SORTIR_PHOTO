# 🚀 PANDUAN CEPAT - AI Photo Sorter with Auto Clustering

## 🌟 FITUR BARU: AUTO CLUSTERING WAJAH!
**AI otomatis mengelompokkan orang yang sama ke folder terpisah**

## 📋 Langkah-langkah Instalasi & Penggunaan

### 1️⃣ INSTALASI (Pilih salah satu)

#### Otomatis (Windows)
```
Klik 2x: setup.bat
```

#### Manual
```
pip install opencv-python pillow numpy
```

### 2️⃣ MENJALANKAN APLIKASI

#### ⭐ Auto Clustering (RECOMMENDED)
```
python photo_sorter_advanced.py
```

#### OpenCV Sederhana
```
python photo_sorter_opencv.py
```

#### Advanced Recognition (butuh face_recognition)
```
python photo_sorter_gui.py
```

### 3️⃣ CARA PAKAI AUTO CLUSTERING
1. ✅ **Aktifkan "Auto Clustering"** 
2. ⚙️ **Atur sensitivitas** (0.5 = optimal)
3. **Browse** → Pilih folder foto sumber
4. **Browse** → Pilih folder tujuan  
5. **🚀 Mulai Auto Clustering**
6. **Tunggu 3 fase**: Deteksi → Clustering → Sortir

### 4️⃣ TESTING DENGAN DEMO
- Folder `demo_photos` berisi gambar untuk testing
- Gunakan sebagai folder sumber untuk testing aplikasi

## 📁 HASIL AUTO CLUSTERING

```
📂 Folder Tujuan/
├── 📁 Person_01/              # Semua foto orang pertama
├── 📁 Person_02/              # Semua foto orang kedua
├── 📁 Person_03/              # Semua foto orang ketiga
├── 📁 Unknown_Unique_Face/    # Wajah unik yang tidak bisa dikelompokkan
└── 📁 No_Face_Detected/       # Foto tanpa wajah (landscape, dll)
```

## ⚙️ PENGATURAN AUTO CLUSTERING

### Sensitivitas Clustering:
- **0.1-0.3**: Ketat - Banyak kelompok terpisah
- **0.4-0.6**: Optimal - Seimbang (RECOMMENDED)
- **0.7-0.8**: Longgar - Sedikit kelompok besar

### Ukuran Wajah Minimum:
- **30-50px**: Sangat sensitif (deteksi wajah kecil)
- **50-100px**: Seimbang (RECOMMENDED)
- **100-200px**: Konservatif (hanya wajah besar)

## 🆘 TROUBLESHOOTING

### Terlalu banyak kelompok terpisah?
- Naikkan sensitivitas clustering ke 0.6-0.8
- Foto mungkin berkualitas sangat baik

### Orang berbeda masuk grup sama?  
- Turunkan sensitivitas clustering ke 0.2-0.4
- Periksa kualitas dan pencahayaan foto

### Tidak ada wajah terdeteksi?
- Turunkan "Ukuran wajah minimum" ke 30-50px
- Pastikan foto berkualitas baik

### Error saat install?
```bash
pip install --upgrade pip
pip install opencv-python pillow numpy
```

## 🎯 TIPS PRO

### 📸 Untuk Hasil Terbaik:
1. **Foto berkualitas baik** (minimal 640x480)
2. **Pencahayaan cukup** (tidak terlalu gelap)
3. **Wajah jelas terlihat** (tidak tertutup/miring)

### ⚙️ Workflow Optimal:
1. **Test dengan 10-20 foto** dulu
2. **Adjust sensitivitas** berdasarkan hasil
3. **Proses batch besar** setelah setting optimal

### 🚀 Performa:
- **100 foto**: ~2-3 menit
- **500 foto**: ~8-12 menit
- **1000 foto**: ~15-25 menit

## 🎯 COCOK UNTUK
- 💒 Wedding photography (sortir tamu per orang)
- 🎉 Family events (kelompokkan anggota keluarga)
- 📷 Professional photoshoot (organisir model/talent)
- 📱 Personal gallery cleanup (ribuan foto jadi rapi)

## 🔥 3 VERSI TERSEDIA

### 1. **photo_sorter_advanced.py** ⭐
- **Auto Clustering Wajah**
- **Mudah install (OpenCV only)**
- **Hasil: Person_01, Person_02, dst**

### 2. **photo_sorter_opencv.py**
- **Sortir berdasarkan jumlah wajah**
- **Ringan & cepat**
- **Hasil: Single_Face, Multiple_Faces_X**

### 3. **photo_sorter_gui.py** 
- **Database wajah dikenal + Auto Clustering**
- **Paling canggih**
- **Butuh instalasi face_recognition**

---
✨ **Auto Clustering siap pakai dalam 2 menit!** ✨
