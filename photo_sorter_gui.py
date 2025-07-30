# AI Photo Sorter - Aplikasi Sortir Foto Berdasarkan Wajah
# Created with GUI yang User-Friendly

import os
import cv2
import face_recognition
import numpy as np
from shutil import copyfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import threading
import json
from datetime import datetime
from collections import defaultdict

class PhotoSorterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Photo Sorter - Sortir Foto Berdasarkan Wajah")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.source_folder = tk.StringVar()
        self.destination_folder = tk.StringVar()
        self.known_faces_db = {}  # Dictionary to store known face encodings
        self.processing = False
        self.auto_cluster = tk.BooleanVar(value=True)  # Auto clustering faces
        self.cluster_tolerance = tk.DoubleVar(value=0.6)  # Face similarity threshold
        
        # For auto clustering
        self.all_face_encodings = []  # Store all face encodings during processing
        self.face_file_mapping = []   # Map encodings to their source files
        
        # Load known faces database
        self.load_known_faces_db()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="🤖 AI Photo Sorter", 
                              font=("Arial", 20, "bold"), 
                              bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(self.root, text="Sortir Foto Otomatis Berdasarkan Pengenalan Wajah", 
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
        
        # Known faces management
        faces_frame = tk.LabelFrame(main_frame, text="👤 Manajemen Wajah", 
                                  font=("Arial", 12, "bold"), 
                                  bg='#f0f0f0', padx=10, pady=10)
        faces_frame.pack(fill='x', pady=10)
        
        # Auto clustering option
        tk.Checkbutton(faces_frame, text="🤖 Auto Clustering Wajah (Kelompokkan wajah mirip otomatis)", 
                      variable=self.auto_cluster, bg='#f0f0f0',
                      font=("Arial", 10, "bold")).pack(anchor='w', padx=5)
        
        # Clustering tolerance
        tolerance_frame = tk.Frame(faces_frame, bg='#f0f0f0')
        tolerance_frame.pack(anchor='w', padx=20, pady=5)
        tk.Label(tolerance_frame, text="Sensitivitas pengelompokan:", 
                bg='#f0f0f0', font=("Arial", 9)).pack(side='left')
        tk.Scale(tolerance_frame, from_=0.3, to=0.9, resolution=0.1, orient='horizontal',
                variable=self.cluster_tolerance, bg='#f0f0f0', length=150).pack(side='left', padx=10)
        tk.Label(tolerance_frame, text="(0.3=Ketat, 0.9=Longgar)", 
                bg='#f0f0f0', font=("Arial", 8), fg='#666').pack(side='left')
        
        # Manual face management (only show when auto clustering is off)
        manual_frame = tk.Frame(faces_frame, bg='#f0f0f0')
        manual_frame.pack(anchor='w', padx=5, pady=5)
        
        tk.Button(manual_frame, text="Tambah Wajah Dikenal", 
                 command=self.add_known_face,
                 bg='#FF9800', fg='white', font=("Arial", 10),
                 relief='flat', padx=15).pack(side='left', padx=5)
        tk.Button(manual_frame, text="Lihat Wajah Tersimpan", 
                 command=self.view_known_faces,
                 bg='#9C27B0', fg='white', font=("Arial", 10),
                 relief='flat', padx=15).pack(side='left', padx=5)
        
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
        self.log_message("Selamat datang di AI Photo Sorter!")
        self.log_message("🤖 Mode Auto Clustering: AI akan mengelompokkan wajah mirip secara otomatis")
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
            
    def add_known_face(self):
        image_file = filedialog.askopenfilename(
            title="Pilih Foto Wajah yang Dikenal",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if image_file:
            name = simpledialog.askstring("Nama Orang", 
                                        "Masukkan nama untuk wajah ini:",
                                        initialvalue="")
            if name and name.strip():
                try:
                    self.log_message(f"Memproses wajah untuk: {name}")
                    # Load and encode the face
                    image = face_recognition.load_image_file(image_file)
                    face_encodings = face_recognition.face_encodings(image)
                    
                    if face_encodings:
                        self.known_faces_db[name.strip()] = face_encodings[0].tolist()
                        self.save_known_faces_db()
                        self.log_message(f"✓ Wajah '{name}' berhasil ditambahkan!")
                        messagebox.showinfo("Sukses", f"Wajah '{name}' berhasil ditambahkan ke database!")
                    else:
                        messagebox.showerror("Error", "Tidak ada wajah yang terdeteksi dalam foto!\nPastikan foto menunjukkan wajah dengan jelas.")
                        self.log_message("✗ Gagal mendeteksi wajah dalam foto")
                except Exception as e:
                    messagebox.showerror("Error", f"Gagal memproses foto: {str(e)}")
                    self.log_message(f"✗ Error: {str(e)}")
                    
    def view_known_faces(self):
        if not self.known_faces_db:
            messagebox.showinfo("Info", "Belum ada wajah yang tersimpan dalam database.")
            return
            
        faces_window = tk.Toplevel(self.root)
        faces_window.title("Daftar Wajah Tersimpan")
        faces_window.geometry("450x350")
        faces_window.configure(bg='#f0f0f0')
        
        tk.Label(faces_window, text="👥 Daftar Wajah yang Tersimpan:", 
                font=("Arial", 14, "bold"), bg='#f0f0f0').pack(pady=10)
        
        frame = tk.Frame(faces_window, bg='#f0f0f0')
        frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        listbox = tk.Listbox(frame, font=("Arial", 11), height=12)
        listbox.pack(fill='both', expand=True)
        
        for name in self.known_faces_db.keys():
            listbox.insert(tk.END, f"• {name}")
            
        def delete_selected():
            selection = listbox.curselection()
            if selection:
                selected_text = listbox.get(selection[0])
                name = selected_text.replace("• ", "")
                if messagebox.askyesno("Konfirmasi", f"Hapus wajah '{name}' dari database?"):
                    del self.known_faces_db[name]
                    self.save_known_faces_db()
                    listbox.delete(selection[0])
                    self.log_message(f"Wajah '{name}' dihapus dari database")
                    
        button_frame = tk.Frame(faces_window, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="🗑️ Hapus Terpilih", 
                 command=delete_selected, bg='#f44336', fg='white',
                 font=("Arial", 10), relief='flat', padx=15).pack(side='left', padx=5)
        tk.Button(button_frame, text="✖️ Tutup", 
                 command=faces_window.destroy, bg='#666', fg='white',
                 font=("Arial", 10), relief='flat', padx=15).pack(side='left', padx=5)
        
    def load_known_faces_db(self):
        try:
            if os.path.exists('known_faces.json'):
                with open('known_faces.json', 'r', encoding='utf-8') as f:
                    self.known_faces_db = json.load(f)
                    if self.known_faces_db:
                        print(f"Database wajah dimuat: {len(self.known_faces_db)} wajah")
        except Exception as e:
            self.known_faces_db = {}
            print(f"Error loading database: {e}")
            
    def save_known_faces_db(self):
        try:
            with open('known_faces.json', 'w', encoding='utf-8') as f:
                json.dump(self.known_faces_db, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_message(f"Error menyimpan database wajah: {str(e)}")
            
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
        
    def process_photos(self):
        try:
            source_dir = self.source_folder.get()
            dest_dir = self.destination_folder.get()
            
            # Clear previous clustering data
            self.all_face_encodings = []
            self.face_file_mapping = []
            
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
                
            mode = "Auto Clustering" if self.auto_cluster.get() else "Manual Recognition"
            self.log_message(f"📊 Total foto untuk diproses: {len(image_files)}")
            self.log_message(f"🤖 Mode: {mode}")
            if self.auto_cluster.get():
                self.log_message(f"⚙️ Sensitivitas clustering: {self.cluster_tolerance.get()}")
            else:
                self.log_message(f"📊 Wajah yang dikenal dalam database: {len(self.known_faces_db)}")
            self.log_message("-" * 50)
            
            if self.auto_cluster.get():
                self.process_with_auto_clustering(source_dir, dest_dir, image_files)
            else:
                self.process_with_manual_recognition(source_dir, dest_dir, image_files)
                
        except Exception as e:
            self.log_message(f"❌ Error besar: {str(e)}")
            self.stop_sorting()
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
            
    def process_with_auto_clustering(self, source_dir, dest_dir, image_files):
        """Process photos using automatic face clustering"""
        self.log_message("🔍 FASE 1: Mendeteksi dan mengekstrak semua wajah...")
        
        processed_count = 0
        face_found_count = 0
        total_faces = 0
        
        # Phase 1: Extract all face encodings
        for i, image_file in enumerate(image_files):
            if not self.processing:
                break
                
            try:
                # Update progress for phase 1 (50% of total progress)
                progress = (i / len(image_files)) * 50
                self.progress_var.set(progress)
                self.status_label.config(text=f"Ekstraksi wajah: {image_file}")
                
                # Load and process image
                image_path = os.path.join(source_dir, image_file)
                self.log_message(f"🔍 Memproses: {image_file}")
                
                image = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(image)
                
                if face_locations:
                    face_found_count += 1
                    face_encodings = face_recognition.face_encodings(image, face_locations)
                    
                    for j, face_encoding in enumerate(face_encodings):
                        self.all_face_encodings.append(face_encoding)
                        self.face_file_mapping.append({
                            'file': image_file,
                            'face_index': j,
                            'total_faces': len(face_encodings),
                            'encoding': face_encoding
                        })
                        total_faces += 1
                    
                    self.log_message(f"   ✓ {len(face_encodings)} wajah ditemukan")
                else:
                    # No faces found, copy to "No_Face" folder immediately
                    no_face_folder = os.path.join(dest_dir, "No_Face_Detected")
                    if not os.path.exists(no_face_folder):
                        os.makedirs(no_face_folder)
                    destination_path = os.path.join(no_face_folder, image_file)
                    copyfile(os.path.join(source_dir, image_file), destination_path)
                    self.log_message(f"   ⚠ Tidak ada wajah terdeteksi")
                    
                processed_count += 1
                
            except Exception as e:
                self.log_message(f"   ✗ Error: {str(e)}")
        
        if not self.all_face_encodings:
            self.log_message("❌ Tidak ada wajah yang berhasil diekstrak!")
            self.stop_sorting()
            return
            
        self.log_message(f"✅ FASE 1 Selesai: {total_faces} wajah diekstrak dari {face_found_count} foto")
        self.log_message("-" * 50)
        self.log_message("🤖 FASE 2: Mengelompokkan wajah yang mirip...")
        
        # Phase 2: Cluster faces
        self.progress_var.set(60)
        self.status_label.config(text="Mengelompokkan wajah...")
        
        clusters = self.cluster_faces(self.all_face_encodings)
        unique_clusters = len(set(clusters))
        
        self.log_message(f"✅ Ditemukan {unique_clusters} kelompok wajah unik")
        self.log_message("-" * 50)
        self.log_message("📁 FASE 3: Menyortir foto ke folder...")
        
        # Phase 3: Sort photos into folders
        cluster_counters = defaultdict(int)
        
        for i, (face_data, cluster_id) in enumerate(zip(self.face_file_mapping, clusters)):
            if not self.processing:
                break
                
            try:
                # Update progress for phase 3 (remaining 40%)
                progress = 60 + (i / len(self.face_file_mapping)) * 40
                self.progress_var.set(progress)
                
                image_file = face_data['file']
                face_index = face_data['face_index']
                total_faces_in_image = face_data['total_faces']
                
                # Determine folder name
                if cluster_id == -1:  # Noise/outlier
                    folder_name = "Unknown_Unique_Face"
                else:
                    folder_name = f"Person_{cluster_id + 1:02d}"
                
                # Create folder if it doesn't exist
                person_folder = os.path.join(dest_dir, folder_name)
                if not os.path.exists(person_folder):
                    os.makedirs(person_folder)
                    
                # Generate destination filename
                if total_faces_in_image > 1:
                    filename, ext = os.path.splitext(image_file)
                    destination_file = f"{filename}_wajah_{face_index + 1}{ext}"
                else:
                    destination_file = image_file
                    
                # Check if file already copied (for multiple faces in same image)
                source_path = os.path.join(source_dir, image_file)
                destination_path = os.path.join(person_folder, destination_file)
                
                if not os.path.exists(destination_path):
                    copyfile(source_path, destination_path)
                    cluster_counters[folder_name] += 1
                    
            except Exception as e:
                self.log_message(f"   ✗ Error copying file: {str(e)}")
        
        # Final results
        self.progress_var.set(100)
        self.status_label.config(text="Proses selesai!")
        self.log_message("=" * 50)
        self.log_message("🎉 PROSES AUTO CLUSTERING SELESAI!")
        self.log_message(f"📊 STATISTIK HASIL:")
        self.log_message(f"   • Total foto diproses: {processed_count}")
        self.log_message(f"   • Foto dengan wajah: {face_found_count}")
        self.log_message(f"   • Total wajah ditemukan: {total_faces}")
        self.log_message(f"   • Kelompok wajah unik: {unique_clusters}")
        self.log_message(f"   • Foto tanpa wajah: {processed_count - face_found_count}")
        
        # Show cluster distribution
        self.log_message("📁 DISTRIBUSI KELOMPOK:")
        for folder_name, count in sorted(cluster_counters.items()):
            self.log_message(f"   • {folder_name}: {count} foto")
            
        self.log_message(f"📁 Hasil tersimpan di: {dest_dir}")
        self.log_message("=" * 50)
        
        self.stop_sorting()
        
        # Show summary dialog
        summary = (f"Proses Auto Clustering selesai!\n\n"
                  f"📊 RINGKASAN:\n"
                  f"• Total foto: {processed_count}\n"
                  f"• Foto dengan wajah: {face_found_count}\n"
                  f"• Total wajah: {total_faces}\n"
                  f"• Kelompok unik: {unique_clusters}\n\n"
                  f"📁 Hasil tersimpan di:\n{dest_dir}")
        
        messagebox.showinfo("Auto Clustering Selesai", summary)
        
        # Ask if user wants to open result folder
        if messagebox.askyesno("Buka Folder", "Ingin membuka folder hasil sortir?"):
            os.startfile(dest_dir)
            
    def cluster_faces(self, face_encodings):
        """Cluster faces using distance-based grouping"""
        if not face_encodings:
            return []
            
        self.log_message(f"🔄 Menghitung similarity matrix untuk {len(face_encodings)} wajah...")
        
        # Calculate distance matrix
        distances = []
        for i, encoding1 in enumerate(face_encodings):
            row = []
            for j, encoding2 in enumerate(face_encodings):
                if i == j:
                    distance = 0.0
                else:
                    distance = face_recognition.face_distance([encoding1], encoding2)[0]
                row.append(distance)
            distances.append(row)
            
        # Simple clustering based on distance threshold
        tolerance = self.cluster_tolerance.get()
        clusters = [-1] * len(face_encodings)  # -1 means unassigned
        current_cluster = 0
        
        for i in range(len(face_encodings)):
            if clusters[i] != -1:  # Already assigned
                continue
                
            # Create new cluster
            clusters[i] = current_cluster
            cluster_members = [i]
            
            # Find all faces similar to this one
            for j in range(i + 1, len(face_encodings)):
                if clusters[j] != -1:  # Already assigned
                    continue
                    
                # Check if similar to any member of current cluster
                is_similar = False
                for member in cluster_members:
                    if distances[member][j] <= tolerance:
                        is_similar = True
                        break
                        
                if is_similar:
                    clusters[j] = current_cluster
                    cluster_members.append(j)
                    
            current_cluster += 1
            
        self.log_message(f"✅ Clustering selesai: {current_cluster} kelompok ditemukan")
        return clusters
        
    def process_with_manual_recognition(self, source_dir, dest_dir, image_files):
        """Process photos using manual known faces database"""
        processed_count = 0
        face_found_count = 0
        known_face_count = 0
        unknown_person_counter = 1
        
        for i, image_file in enumerate(image_files):
            if not self.processing:
                break
                
            try:
                # Update progress
                progress = (i / len(image_files)) * 100
                self.progress_var.set(progress)
                self.status_label.config(text=f"Memproses: {image_file}")
                
                # Load and process image
                image_path = os.path.join(source_dir, image_file)
                self.log_message(f"🔍 Memproses: {image_file}")
                
                image = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(image)
                
                if face_locations:
                    face_found_count += 1
                    face_encodings = face_recognition.face_encodings(image, face_locations)
                    
                    for j, face_encoding in enumerate(face_encodings):
                        # Find matching known face
                        matched_name = self.find_matching_face(face_encoding)
                        
                        if matched_name:
                            folder_name = matched_name
                            known_face_count += 1
                            self.log_message(f"   ✓ Wajah dikenali: {matched_name}")
                        else:
                            # Create numbered unknown folder
                            existing_unknown = [d for d in os.listdir(dest_dir) 
                                              if d.startswith("Unknown_Person_")]
                            if existing_unknown:
                                numbers = []
                                for folder in existing_unknown:
                                    try:
                                        num = int(folder.split("_")[-1])
                                        numbers.append(num)
                                    except:
                                        continue
                                unknown_person_counter = max(numbers) + 1 if numbers else 1
                            
                            folder_name = f"Unknown_Person_{unknown_person_counter}"
                            unknown_person_counter += 1
                            self.log_message(f"   ? Wajah tidak dikenal: {folder_name}")
                            
                        # Create folder if it doesn't exist
                        person_folder = os.path.join(dest_dir, folder_name)
                        if not os.path.exists(person_folder):
                            os.makedirs(person_folder)
                            
                        # Copy image to appropriate folder
                        if len(face_encodings) > 1:
                            # Multiple faces in image
                            filename, ext = os.path.splitext(image_file)
                            destination_file = f"{filename}_wajah_{j+1}{ext}"
                        else:
                            destination_file = image_file
                            
                        destination_path = os.path.join(person_folder, destination_file)
                        copyfile(image_path, destination_path)
                        
                    if len(face_encodings) > 1:
                        self.log_message(f"   📁 {len(face_encodings)} wajah dalam 1 foto")
                else:
                    # No faces found, copy to "No_Face" folder
                    no_face_folder = os.path.join(dest_dir, "No_Face_Detected")
                    if not os.path.exists(no_face_folder):
                        os.makedirs(no_face_folder)
                    destination_path = os.path.join(no_face_folder, image_file)
                    copyfile(image_path, destination_path)
                    self.log_message(f"   ⚠ Tidak ada wajah terdeteksi")
                    
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
        self.log_message(f"   • Wajah yang dikenal: {known_face_count}")
        self.log_message(f"   • Foto tanpa wajah: {processed_count - face_found_count}")
        self.log_message(f"📁 Hasil tersimpan di: {dest_dir}")
        self.log_message("=" * 50)
        
        self.stop_sorting()
        messagebox.showinfo("Selesai", 
                          f"Proses sortir foto telah selesai!\n\n"
                          f"Total foto: {processed_count}\n"
                          f"Foto dengan wajah: {face_found_count}\n"
                          f"Wajah dikenal: {known_face_count}\n\n"
                          f"Hasil tersimpan di:\n{dest_dir}")
            
    def find_matching_face(self, face_encoding):
        """Find matching face from known faces database"""
        if not self.known_faces_db:
            return None
            
        for name, known_encoding in self.known_faces_db.items():
            try:
                # Convert back to numpy array
                known_face_array = np.array(known_encoding)
                
                # Compare faces with tolerance
                matches = face_recognition.compare_faces([known_face_array], face_encoding, tolerance=0.6)
                
                if matches[0]:
                    return name
            except Exception as e:
                continue
                
        return None

def main():
    """Main function to run the application"""
    try:
        # Create the main window
        root = tk.Tk()
        
        # Set window icon if available
        try:
            root.iconbitmap("icon.ico")
        except:
            pass
            
        # Create and run the application
        app = PhotoSorterGUI(root)
        
        # Center the window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Start the GUI
        root.mainloop()
        
    except ImportError as e:
        print("Error: Beberapa library yang diperlukan tidak ditemukan!")
        print("Silakan install library berikut:")
        print("pip install opencv-python face-recognition pillow numpy")
        print(f"Detail error: {e}")
    except Exception as e:
        print(f"Error menjalankan aplikasi: {e}")

if __name__ == "__main__":
    main()
