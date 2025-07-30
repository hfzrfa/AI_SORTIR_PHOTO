# AI Photo Sorter - Versi OpenCV (Tanpa Face Recognition)
# Aplikasi Sortir Foto Berdasarkan Deteksi Wajah

import os
import cv2
import numpy as np
from shutil import copyfile, move
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import threading
import json
from datetime import datetime
import hashlib

class PhotoSorterOpenCV:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Photo Sorter - Deteksi Wajah dengan OpenCV")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.source_folder = tk.StringVar()
        self.destination_folder = tk.StringVar()
        self.processing = False
        self.group_by_faces = tk.BooleanVar(value=True)
        self.min_face_size = tk.IntVar(value=50)
        
        # Initialize face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="🤖 AI Photo Sorter (OpenCV)", 
                              font=("Arial", 20, "bold"), 
                              bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(self.root, text="Sortir Foto Otomatis Berdasarkan Deteksi Wajah", 
                                 font=("Arial", 10), 
                                 bg='#f0f0f0', fg='#666')
        subtitle_label.pack(pady=(0, 20))
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Source folder selection
        source_frame = tk.LabelFrame(main_frame, text="📁 Pilih Folder Foto Sumber", 
                                   font=("Arial", 12, "bold"), 
                                   bg='#f0f0f0', padx=10, pady=10)
        source_frame.pack(fill='x', pady=10)
        
        tk.Entry(source_frame, textvariable=self.source_folder, 
                font=("Arial", 10), width=60).pack(side='left', padx=5)
        tk.Button(source_frame, text="Browse", command=self.select_source_folder,
                 bg='#4CAF50', fg='white', font=("Arial", 10), 
                 relief='flat', padx=15).pack(side='right', padx=5)
        
        # Destination folder selection
        dest_frame = tk.LabelFrame(main_frame, text="📂 Pilih Folder Tujuan", 
                                 font=("Arial", 12, "bold"), 
                                 bg='#f0f0f0', padx=10, pady=10)
        dest_frame.pack(fill='x', pady=10)
        
        tk.Entry(dest_frame, textvariable=self.destination_folder, 
                font=("Arial", 10), width=60).pack(side='left', padx=5)
        tk.Button(dest_frame, text="Browse", command=self.select_destination_folder,
                 bg='#2196F3', fg='white', font=("Arial", 10), 
                 relief='flat', padx=15).pack(side='right', padx=5)
        
        # Settings frame
        settings_frame = tk.LabelFrame(main_frame, text="⚙️ Pengaturan Deteksi", 
                                     font=("Arial", 12, "bold"), 
                                     bg='#f0f0f0', padx=10, pady=10)
        settings_frame.pack(fill='x', pady=10)
        
        # Group by faces checkbox
        tk.Checkbutton(settings_frame, text="Kelompokkan berdasarkan jumlah wajah", 
                      variable=self.group_by_faces, bg='#f0f0f0',
                      font=("Arial", 10)).pack(anchor='w', padx=5)
        
        # Min face size setting
        size_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        size_frame.pack(anchor='w', padx=5, pady=5)
        tk.Label(size_frame, text="Ukuran wajah minimum (px):", 
                bg='#f0f0f0', font=("Arial", 10)).pack(side='left')
        tk.Scale(size_frame, from_=30, to=200, orient='horizontal',
                variable=self.min_face_size, bg='#f0f0f0', length=200).pack(side='left', padx=10)
        
        # Progress frame
        progress_frame = tk.Frame(main_frame, bg='#f0f0f0')
        progress_frame.pack(fill='x', pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(pady=5)
        
        self.status_label = tk.Label(progress_frame, text="Siap untuk memproses foto", 
                                   font=("Arial", 10), bg='#f0f0f0', fg='#666')
        self.status_label.pack()
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(button_frame, text="🚀 Mulai Sortir Foto", 
                                    command=self.start_sorting,
                                    bg='#4CAF50', fg='white', 
                                    font=("Arial", 12, "bold"),
                                    padx=20, pady=10, relief='flat')
        self.start_button.pack(side='left', padx=10)
        
        self.stop_button = tk.Button(button_frame, text="⏹️ Stop", 
                                   command=self.stop_sorting,
                                   bg='#f44336', fg='white', 
                                   font=("Arial", 12, "bold"),
                                   padx=20, pady=10, relief='flat',
                                   state='disabled')
        self.stop_button.pack(side='left', padx=10)
        
        # Results text area
        results_frame = tk.LabelFrame(main_frame, text="📊 Hasil Proses dan Log", 
                                    font=("Arial", 12, "bold"), 
                                    bg='#f0f0f0')
        results_frame.pack(fill='both', expand=True, pady=10)
        
        self.results_text = tk.Text(results_frame, height=8, font=("Consolas", 9),
                                   bg='#f8f8f8', fg='#333')
        scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Initial message
        self.log_message("Selamat datang di AI Photo Sorter (OpenCV Version)!")
        self.log_message("Versi ini menggunakan OpenCV untuk deteksi wajah yang lebih mudah diinstall.")
        self.log_message("Pilih folder sumber dan tujuan, lalu klik 'Mulai Sortir Foto'")
        
    def select_source_folder(self):
        folder = filedialog.askdirectory(title="Pilih Folder yang Berisi Foto-foto")
        if folder:
            self.source_folder.set(folder)
            # Count images in folder
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
            image_count = len([f for f in os.listdir(folder) 
                             if f.lower().endswith(image_extensions)])
            self.log_message(f"Folder sumber dipilih: {folder}")
            self.log_message(f"Ditemukan {image_count} file gambar")
            
    def select_destination_folder(self):
        folder = filedialog.askdirectory(title="Pilih Folder Tujuan untuk Menyimpan Hasil")
        if folder:
            self.destination_folder.set(folder)
            self.log_message(f"Folder tujuan dipilih: {folder}")
            
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update()
        
    def start_sorting(self):
        if not self.source_folder.get() or not self.destination_folder.get():
            messagebox.showerror("Error", 
                               "Silakan pilih folder sumber dan folder tujuan terlebih dahulu!")
            return
            
        if not os.path.exists(self.source_folder.get()):
            messagebox.showerror("Error", "Folder sumber tidak ditemukan!")
            return
            
        self.processing = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.progress_var.set(0)
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.log_message("=== MEMULAI PROSES SORTIR FOTO ===")
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_photos)
        thread.daemon = True
        thread.start()
        
    def stop_sorting(self):
        self.processing = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.log_message("⏹️ Proses dihentikan oleh pengguna")
        
    def detect_faces(self, image_path):
        """Detect faces in image using OpenCV"""
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                return 0, []
                
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(self.min_face_size.get(), self.min_face_size.get())
            )
            
            return len(faces), faces
            
        except Exception as e:
            self.log_message(f"Error detecting faces in {os.path.basename(image_path)}: {str(e)}")
            return 0, []
            
    def process_photos(self):
        try:
            source_dir = self.source_folder.get()
            dest_dir = self.destination_folder.get()
            
            # Ensure destination folder exists
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
                self.log_message(f"Folder tujuan dibuat: {dest_dir}")
                
            # Get all image files
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
            image_files = [f for f in os.listdir(source_dir) 
                          if f.lower().endswith(image_extensions)]
            
            if not image_files:
                self.log_message("❌ Tidak ada file gambar ditemukan dalam folder!")
                self.stop_sorting()
                return
                
            self.log_message(f"📊 Total foto untuk diproses: {len(image_files)}")
            self.log_message(f"⚙️ Ukuran wajah minimum: {self.min_face_size.get()}px")
            self.log_message(f"⚙️ Kelompokkan berdasarkan jumlah wajah: {'Ya' if self.group_by_faces.get() else 'Tidak'}")
            self.log_message("-" * 50)
            
            processed_count = 0
            face_found_count = 0
            stats = {
                'no_face': 0,
                'single_face': 0,
                'multiple_faces': 0
            }
            
            for i, image_file in enumerate(image_files):
                if not self.processing:
                    break
                    
                try:
                    # Update progress
                    progress = (i / len(image_files)) * 100
                    self.progress_var.set(progress)
                    self.status_label.config(text=f"Memproses: {image_file}")
                    
                    # Process image
                    image_path = os.path.join(source_dir, image_file)
                    self.log_message(f"🔍 Memproses: {image_file}")
                    
                    # Detect faces
                    face_count, faces = self.detect_faces(image_path)
                    
                    # Determine destination folder
                    if face_count == 0:
                        folder_name = "No_Face_Detected"
                        stats['no_face'] += 1
                        self.log_message(f"   ⚠ Tidak ada wajah terdeteksi")
                    elif face_count == 1:
                        if self.group_by_faces.get():
                            folder_name = "Single_Face"
                        else:
                            folder_name = "With_Faces"
                        stats['single_face'] += 1
                        face_found_count += 1
                        self.log_message(f"   ✓ 1 wajah terdeteksi")
                    else:
                        if self.group_by_faces.get():
                            folder_name = f"Multiple_Faces_{face_count}"
                        else:
                            folder_name = "With_Faces"
                        stats['multiple_faces'] += 1
                        face_found_count += 1
                        self.log_message(f"   ✓ {face_count} wajah terdeteksi")
                    
                    # Create destination folder
                    dest_folder = os.path.join(dest_dir, folder_name)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    
                    # Copy file
                    dest_path = os.path.join(dest_folder, image_file)
                    copyfile(image_path, dest_path)
                    
                    processed_count += 1
                    
                except Exception as e:
                    self.log_message(f"   ✗ Error: {str(e)}")
                    
            # Final results
            self.progress_var.set(100)
            self.status_label.config(text="Proses selesai!")
            self.log_message("=" * 50)
            self.log_message("🎉 PROSES SORTIR FOTO SELESAI!")
            self.log_message(f"📊 STATISTIK HASIL:")
            self.log_message(f"   • Total foto diproses: {processed_count}")
            self.log_message(f"   • Foto dengan wajah: {face_found_count}")
            self.log_message(f"   • Foto tanpa wajah: {stats['no_face']}")
            self.log_message(f"   • Foto dengan 1 wajah: {stats['single_face']}")
            self.log_message(f"   • Foto dengan banyak wajah: {stats['multiple_faces']}")
            self.log_message(f"📁 Hasil tersimpan di: {dest_dir}")
            self.log_message("=" * 50)
            
            self.stop_sorting()
            
            # Create summary report
            summary = (f"Proses sortir foto selesai!\n\n"
                      f"📊 RINGKASAN:\n"
                      f"• Total foto: {processed_count}\n"
                      f"• Foto dengan wajah: {face_found_count}\n"
                      f"• Foto tanpa wajah: {stats['no_face']}\n"
                      f"• Foto dengan 1 wajah: {stats['single_face']}\n"
                      f"• Foto dengan banyak wajah: {stats['multiple_faces']}\n\n"
                      f"📁 Hasil tersimpan di:\n{dest_dir}")
            
            messagebox.showinfo("Proses Selesai", summary)
            
            # Ask if user wants to open result folder
            if messagebox.askyesno("Buka Folder", "Ingin membuka folder hasil sortir?"):
                os.startfile(dest_dir)
            
        except Exception as e:
            self.log_message(f"❌ Error besar: {str(e)}")
            self.stop_sorting()
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

def main():
    """Main function to run the application"""
    try:
        # Test OpenCV installation
        cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Create the main window
        root = tk.Tk()
        
        # Set window icon if available
        try:
            root.iconbitmap("icon.ico")
        except:
            pass
            
        # Create and run the application
        app = PhotoSorterOpenCV(root)
        
        # Center the window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Start the GUI
        root.mainloop()
        
    except ImportError as e:
        print("Error: OpenCV tidak ditemukan!")
        print("Silakan install OpenCV dengan command:")
        print("pip install opencv-python")
        print(f"Detail error: {e}")
    except Exception as e:
        print(f"Error menjalankan aplikasi: {e}")

if __name__ == "__main__":
    main()
