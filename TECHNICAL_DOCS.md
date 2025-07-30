# 🛠️ Dokumentasi Teknis - AI Photo Sorter

## 📂 Struktur Project

```
📁 SORTIR PHOTO/
├── 📄 photo_sorter_opencv.py     # Aplikasi utama (OpenCV)
├── 📄 photo_sorter_gui.py        # Aplikasi advanced (Face Recognition)
├── 📄 create_demo.py             # Generator gambar demo
├── 📄 requirements.txt           # Dependencies
├── 📄 README.md                  # Dokumentasi lengkap
├── 📄 QUICK_START.md            # Panduan cepat
├── 📄 setup.bat                 # Script instalasi
├── 📄 run.bat                   # Script menjalankan aplikasi
├── 📄 demo.bat                  # Script demo
└── 📁 demo_photos/              # Folder gambar demo
    ├── 🖼️ landscape.jpg
    ├── 🖼️ single_face.jpg
    ├── 🖼️ group_photo.jpg
    └── 🖼️ no_face.jpg
```

## 🔧 Teknologi yang Digunakan

### Core Libraries
- **OpenCV**: Deteksi wajah menggunakan Haar Cascade
- **tkinter**: GUI framework (built-in Python)
- **PIL/Pillow**: Image processing
- **NumPy**: Array operations

### Algoritma Deteksi Wajah
- **Haar Cascade Classifier** (`haarcascade_frontalface_default.xml`)
- **Scale Factor**: 1.1 (default)
- **Min Neighbors**: 5 (default)
- **Min Size**: User-configurable (30-200px)

## 🏗️ Arsitektur Aplikasi

### Class Structure
```python
PhotoSorterOpenCV
├── __init__()              # Inisialisasi GUI dan variabel
├── create_widgets()        # Membuat elemen GUI
├── select_source_folder()  # Handler pemilihan folder sumber
├── select_destination_folder() # Handler pemilihan folder tujuan
├── log_message()          # Logging ke text area
├── start_sorting()        # Memulai proses sorting
├── stop_sorting()         # Menghentikan proses
├── detect_faces()         # Deteksi wajah dalam gambar
└── process_photos()       # Thread processing utama
```

### Threading Model
- **Main Thread**: GUI dan user interaction
- **Worker Thread**: Image processing (prevent GUI freeze)
- **Progress Updates**: Real-time via threading-safe methods

## 🎯 Algoritma Sorting

### 1. Input Processing
```python
image_files = [f for f in os.listdir(source_dir) 
              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))]
```

### 2. Face Detection
```python
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(min_size, min_size)
)
```

### 3. Categorization Logic
```python
if face_count == 0:
    folder = "No_Face_Detected"
elif face_count == 1:
    folder = "Single_Face" if group_by_faces else "With_Faces"
else:
    folder = f"Multiple_Faces_{face_count}" if group_by_faces else "With_Faces"
```

### 4. File Operations
- **Copy**: Preserve original files
- **Directory Creation**: Auto-create destination folders
- **Error Handling**: Skip problematic files, log errors

## ⚙️ Configuration Parameters

### User-Configurable
- `source_folder`: Input directory path
- `destination_folder`: Output directory path
- `group_by_faces`: Boolean (group by face count)
- `min_face_size`: Integer (30-200px)

### Internal Parameters
- `scaleFactor`: 1.1 (fixed)
- `minNeighbors`: 5 (fixed)
- `image_extensions`: Tuple of supported formats

## 🔍 Face Detection Parameters

### Scale Factor (1.1)
- **Purpose**: Image pyramid scaling
- **Lower values**: More accurate, slower
- **Higher values**: Faster, less accurate

### Min Neighbors (5)
- **Purpose**: Minimum rectangles for valid detection
- **Lower values**: More detections, more false positives
- **Higher values**: Fewer detections, more reliable

### Min Size (User-configurable)
- **30-50px**: Very sensitive, detects small faces
- **50-100px**: Balanced, good for most photos
- **100-200px**: Less sensitive, only large faces

## 🚀 Performance Considerations

### Memory Usage
- **Image Loading**: One image at a time
- **Processing**: Grayscale conversion reduces memory
- **GUI Updates**: Throttled to prevent lag

### Processing Speed
- **Factors**: Image resolution, face count, min_size setting
- **Optimization**: Single-threaded processing (simplicity)
- **Scalability**: Linear with image count

### Error Handling
```python
try:
    # Image processing
except Exception as e:
    log_message(f"Error: {str(e)}")
    continue  # Skip problematic file
```

## 🔧 Customization Guide

### Menambah Format Gambar
```python
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
```

### Mengubah Parameter Deteksi
```python
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.05,    # Lebih akurat tapi lambat
    minNeighbors=3,      # Lebih sensitif
    minSize=(20, 20)     # Deteksi wajah sangat kecil
)
```

### Custom Folder Naming
```python
if face_count == 1:
    folder_name = f"Solo_Person_{datetime.now().strftime('%Y%m%d')}"
elif face_count > 1:
    folder_name = f"Group_{face_count}people"
```

## 🐛 Debugging Guide

### Common Issues
1. **No faces detected**: Lower min_size threshold
2. **Too many false positives**: Increase min_size or minNeighbors
3. **GUI freezing**: Check threading implementation
4. **File permission errors**: Check folder write permissions

### Logging Levels
```python
# Debug mode
DEBUG = True
if DEBUG:
    print(f"Processing {image_file}, faces found: {face_count}")
```

## 📊 Testing Strategy

### Unit Tests
- Face detection accuracy
- File operations
- GUI component functionality

### Integration Tests
- End-to-end workflow
- Error handling
- Performance benchmarks

### Demo Data
- `demo_photos/`: Prepared test images
- Known expected results for validation

## 🔄 Future Enhancements

### Potential Features
1. **Batch Processing**: Multiple source folders
2. **Image Filters**: Quality, blur detection
3. **Export Reports**: CSV/JSON results summary
4. **Cloud Integration**: Google Photos, OneDrive sync
5. **Advanced Sorting**: Age estimation, emotion detection

### Performance Improvements
1. **Multi-threading**: Parallel image processing
2. **GPU Acceleration**: OpenCV DNN modules
3. **Caching**: Pre-computed face detections
4. **Progressive Loading**: Lazy image loading

---
**Dokumentasi dibuat untuk memudahkan maintenance dan pengembangan lebih lanjut**
