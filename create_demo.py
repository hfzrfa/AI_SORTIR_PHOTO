import cv2
import numpy as np
import os

def create_demo_images():
    """Buat beberapa gambar demo untuk testing"""
    demo_folder = "demo_photos"
    if not os.path.exists(demo_folder):
        os.makedirs(demo_folder)
    
    print("Membuat gambar demo untuk testing...")
    
    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Buat gambar dengan berbagai skenario
    images = [
        ("landscape.jpg", create_landscape()),
        ("single_face.jpg", create_single_face()),
        ("group_photo.jpg", create_group_photo()),
        ("no_face.jpg", create_abstract()),
    ]
    
    for filename, image in images:
        cv2.imwrite(os.path.join(demo_folder, filename), image)
        print(f"✓ Dibuat: {filename}")
    
    print(f"\nGambar demo tersimpan di folder: {demo_folder}")
    print("Anda bisa menggunakan folder ini untuk testing aplikasi.")

def create_landscape():
    """Buat gambar landscape sederhana"""
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    
    # Sky (biru)
    img[0:150, :] = [200, 150, 50]
    
    # Ground (hijau)
    img[150:300, :] = [50, 150, 50]
    
    # Sun (kuning)
    cv2.circle(img, (350, 50), 30, (0, 200, 255), -1)
    
    # Mountains
    pts = np.array([[0, 150], [100, 50], [200, 80], [300, 60], [400, 150]], np.int32)
    cv2.fillPoly(img, [pts], (100, 100, 100))
    
    return img

def create_single_face():
    """Buat gambar dengan bentuk wajah sederhana"""
    img = np.ones((300, 300, 3), dtype=np.uint8) * 200
    
    # Face (oval)
    cv2.ellipse(img, (150, 150), (80, 100), 0, 0, 360, (220, 180, 150), -1)
    
    # Eyes
    cv2.circle(img, (120, 130), 8, (0, 0, 0), -1)
    cv2.circle(img, (180, 130), 8, (0, 0, 0), -1)
    
    # Nose
    cv2.line(img, (150, 140), (145, 160), (100, 100, 100), 2)
    
    # Mouth
    cv2.ellipse(img, (150, 180), (20, 10), 0, 0, 180, (100, 50, 50), 2)
    
    return img

def create_group_photo():
    """Buat gambar dengan beberapa bentuk wajah"""
    img = np.ones((400, 500, 3), dtype=np.uint8) * 180
    
    # Face 1
    cv2.ellipse(img, (120, 150), (60, 80), 0, 0, 360, (220, 180, 150), -1)
    cv2.circle(img, (100, 130), 6, (0, 0, 0), -1)
    cv2.circle(img, (140, 130), 6, (0, 0, 0), -1)
    cv2.ellipse(img, (120, 160), (15, 8), 0, 0, 180, (100, 50, 50), 2)
    
    # Face 2
    cv2.ellipse(img, (280, 160), (65, 85), 0, 0, 360, (210, 170, 140), -1)
    cv2.circle(img, (260, 140), 6, (0, 0, 0), -1)
    cv2.circle(img, (300, 140), 6, (0, 0, 0), -1)
    cv2.ellipse(img, (280, 170), (18, 10), 0, 0, 180, (100, 50, 50), 2)
    
    # Face 3
    cv2.ellipse(img, (400, 170), (55, 75), 0, 0, 360, (230, 190, 160), -1)
    cv2.circle(img, (385, 150), 5, (0, 0, 0), -1)
    cv2.circle(img, (415, 150), 5, (0, 0, 0), -1)
    cv2.ellipse(img, (400, 180), (12, 6), 0, 0, 180, (100, 50, 50), 2)
    
    return img

def create_abstract():
    """Buat gambar abstrak tanpa wajah"""
    img = np.random.randint(50, 200, (250, 350, 3), dtype=np.uint8)
    
    # Add some geometric shapes
    cv2.rectangle(img, (50, 50), (150, 150), (255, 100, 100), -1)
    cv2.circle(img, (250, 100), 50, (100, 255, 100), -1)
    triangle = np.array([[200, 200], [250, 150], [300, 200]], np.int32)
    cv2.fillPoly(img, [triangle], (100, 100, 255))
    
    return img

if __name__ == "__main__":
    try:
        create_demo_images()
    except Exception as e:
        print(f"Error: {e}")
        print("Pastikan OpenCV sudah terinstall: pip install opencv-python")
