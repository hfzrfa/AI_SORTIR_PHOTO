# AI Photo Sorter - Advanced Version with Auto Clustering
# Professional Photo Sorting Application with Face Detection and Clustering

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
from collections import defaultdict

class PhotoSorterAdvanced:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Photo Sorter - Advanced Face Clustering")
        self.root.geometry("850x650")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.source_folder = tk.StringVar()
        self.destination_folder = tk.StringVar()
        self.processing = False
        self.group_by_faces = tk.BooleanVar(value=True)
        self.min_face_size = tk.IntVar(value=50)
        self.auto_cluster = tk.BooleanVar(value=True)
        self.cluster_threshold = tk.DoubleVar(value=0.3)
        
        # Face detection and recognition
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # For clustering
        self.all_face_data = []  # Store face data for clustering
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="HFZRFA AI Photo Sorter Advanced", 
                              font=("Arial", 20, "bold"), 
                              bg='#f0f0f0', fg='#1976D2')
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(self.root, text="Professional Photo Organization with Maximum Precision AI Technology", 
                                 font=("Arial", 11), 
                                 bg='#f0f0f0', fg='#666666')
        subtitle_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(self.root, text="Copyright 2025 HFZRFA - Advanced AI Technology", 
                                 font=("Arial", 9, "italic"), 
                                 bg='#f0f0f0', fg='#999999')
        subtitle_label.pack(pady=(0, 20))
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Source folder selection
        source_frame = tk.LabelFrame(main_frame, text="Source Photos Folder", 
                                   font=("Arial", 12, "bold"), 
                                   bg='#f5f5f5', fg='#333333',
                                   padx=10, pady=10)
        source_frame.pack(fill='x', pady=10)
        
        self.source_entry = tk.Entry(source_frame, textvariable=self.source_folder, 
                                   font=("Arial", 10), width=60,
                                   bg='#ffffff', fg='#333333')
        self.source_entry.pack(side='left', padx=5)
        
        self.source_button = tk.Button(source_frame, text="Browse", command=self.select_source_folder,
                                     bg='#107c10', fg='white', font=("Arial", 10), 
                                     relief='flat', padx=15)
        self.source_button.pack(side='right', padx=5)
        
        # Destination folder selection
        dest_frame = tk.LabelFrame(main_frame, text="Destination Folder", 
                                 font=("Arial", 12, "bold"), 
                                 bg='#f5f5f5', fg='#333333',
                                 padx=10, pady=10)
        dest_frame.pack(fill='x', pady=10)
        
        self.dest_entry = tk.Entry(dest_frame, textvariable=self.destination_folder, 
                                 font=("Arial", 10), width=60,
                                 bg='#ffffff', fg='#333333')
        self.dest_entry.pack(side='left', padx=5)
        
        self.dest_button = tk.Button(dest_frame, text="Browse", command=self.select_destination_folder,
                                   bg='#0078d4', fg='white', font=("Arial", 10), 
                                   relief='flat', padx=15)
        self.dest_button.pack(side='right', padx=5)
        
        # Settings frame
        settings_frame = tk.LabelFrame(main_frame, text="AI Configuration", 
                                     font=("Arial", 12, "bold"), 
                                     bg='#f5f5f5', fg='#333333',
                                     padx=10, pady=10)
        settings_frame.pack(fill='x', pady=10)
        
        # Auto clustering option
        self.auto_check = tk.Checkbutton(settings_frame, text="Ultra-Precision Auto Clustering: Group similar faces with maximum accuracy", 
                                       variable=self.auto_cluster, bg='#f5f5f5', fg='#333333',
                                       font=("Arial", 10, "bold"), selectcolor='#ffffff')
        self.auto_check.pack(anchor='w', padx=5)
        
        # Clustering threshold
        cluster_frame = tk.Frame(settings_frame, bg='#f5f5f5')
        cluster_frame.pack(anchor='w', padx=20, pady=5)
        tk.Label(cluster_frame, text="Clustering precision level:", 
                bg='#f5f5f5', fg='#333333', font=("Arial", 9)).pack(side='left')
        self.cluster_scale = tk.Scale(cluster_frame, from_=0.1, to=0.8, resolution=0.1, orient='horizontal',
                                    variable=self.cluster_threshold, bg='#f5f5f5', fg='#333333',
                                    length=150, troughcolor='#ffffff')
        self.cluster_scale.pack(side='left', padx=10)
        tk.Label(cluster_frame, text="(0.1=Ultra Strict, 0.8=Loose)", 
                bg='#f5f5f5', fg='#333333', font=("Arial", 8)).pack(side='left')
        
        # Other settings
        self.group_check = tk.Checkbutton(settings_frame, text="Group by face count", 
                                        variable=self.group_by_faces, bg='#f5f5f5', fg='#333333',
                                        font=("Arial", 10), selectcolor='#ffffff')
        self.group_check.pack(anchor='w', padx=5)
        
        # Min face size setting
        size_frame = tk.Frame(settings_frame, bg='#f5f5f5')
        size_frame.pack(anchor='w', padx=5, pady=5)
        tk.Label(size_frame, text="Minimum face size (px):", 
                bg='#f5f5f5', fg='#333333', font=("Arial", 10)).pack(side='left')
        self.size_scale = tk.Scale(size_frame, from_=30, to=200, orient='horizontal',
                                 variable=self.min_face_size, bg='#f5f5f5', fg='#333333',
                                 length=200, troughcolor='#ffffff')
        self.size_scale.pack(side='left', padx=10)
        
        # Progress frame
        progress_frame = tk.Frame(main_frame, bg='#f0f0f0')
        progress_frame.pack(fill='x', pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(pady=5)
        
        self.status_label = tk.Label(progress_frame, text="Ready to process photos", 
                                   font=("Arial", 10), bg='#f0f0f0', fg='#666')
        self.status_label.pack()
        
        # Control buttons with professional styling
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(button_frame, text="START ULTRA-PRECISION AI SORTING", 
                                    command=self.start_sorting,
                                    bg='#1976D2', fg='white', 
                                    font=("Arial", 14, "bold"),
                                    padx=25, pady=15, relief='raised',
                                    activebackground='#0D47A1', activeforeground='white',
                                    state='normal')  # Always enabled
        self.start_button.pack(side='left', padx=10)
        
        self.stop_button = tk.Button(button_frame, text="STOP PROCESSING", 
                                   command=self.stop_sorting,
                                   bg='#D32F2F', fg='white', 
                                   font=("Arial", 12, "bold"),
                                   padx=20, pady=15, relief='raised',
                                   activebackground='#B71C1C', activeforeground='white',
                                   state='disabled')
        self.stop_button.pack(side='left', padx=10)
        
        # Add demo button for easy testing
        self.demo_button = tk.Button(button_frame, text="DEMO MODE", 
                                   command=self.use_demo_folder,
                                   bg='#FF6F00', fg='white', 
                                   font=("Arial", 11, "bold"),
                                   padx=15, pady=15, relief='raised',
                                   activebackground='#E65100', activeforeground='white')
        self.demo_button.pack(side='left', padx=10)
        
        # Results text area with professional styling
        results_frame = tk.LabelFrame(main_frame, text="Processing Results and Log", 
                                    font=("Arial", 12, "bold"), 
                                    bg='#f5f5f5', fg='#333333')
        results_frame.pack(fill='both', expand=True, pady=10)
        
        self.results_text = tk.Text(results_frame, height=10, font=("Consolas", 9),
                                   bg='#ffffff', fg='#333333')
        scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview,
                               bg='#ffffff')
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Footer with HFZRFA watermark
        footer_frame = tk.Frame(main_frame, bg='#f0f0f0')
        footer_frame.pack(fill='x', pady=(10, 0))
        
        footer_label = tk.Label(footer_frame, 
                               text="Powered by HFZRFA Advanced AI Technology • Professional Photo Organization Solutions", 
                               font=("Arial", 8), bg='#f0f0f0', fg='#666666')
        footer_label.pack()
        
        # Initial professional welcome messages
        self.log_message("Welcome to HFZRFA AI Photo Sorter Advanced - Maximum Precision Edition")
        self.log_message("Ultra-Precision Auto Clustering: AI groups identical faces with maximum accuracy")
        self.log_message("Advanced AI Workflow: Multi-stage face detection -> Enhanced feature extraction -> Precision clustering")
        self.log_message("Professional Interface: Clean, modern design with maximum accuracy algorithms")
        self.log_message("Instructions: Select source and destination folders, configure settings, then start processing")
        self.log_message("Copyright 2025 HFZRFA - Advanced AI Solutions for Professional Photo Management")
        
    def select_source_folder(self):
        folder = filedialog.askdirectory(title="Select Folder Containing Photos")
        if folder:
            self.source_folder.set(folder)
            # Count images in folder
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
            image_count = len([f for f in os.listdir(folder) 
                             if f.lower().endswith(image_extensions)])
            self.log_message(f"Source folder selected: {folder}")
            self.log_message(f"Found {image_count} image files")
            
    def select_destination_folder(self):
        folder = filedialog.askdirectory(title="Select Destination Folder for Results")
        if folder:
            self.destination_folder.set(folder)
            self.log_message(f"Destination folder selected: {folder}")
            
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update()
        
    def use_demo_folder(self):
        """Set up demo folders for easy testing"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        demo_source = os.path.join(current_dir, "demo_photos")
        demo_dest = os.path.join(current_dir, "demo_results")
        
        if os.path.exists(demo_source):
            self.source_folder.set(demo_source)
            self.destination_folder.set(demo_dest)
            self.log_message("Demo folders configured!")
            self.log_message(f"Source: {demo_source}")
            self.log_message(f"Destination: {demo_dest}")
            
            # Ensure demo results folder exists
            if not os.path.exists(demo_dest):
                os.makedirs(demo_dest)
                
            messagebox.showinfo("Demo Ready", 
                              "Demo folders have been configured!\n\n"
                              f"Source: demo_photos\n"
                              f"Destination: demo_results\n\n"
                              "Click 'Start Auto Clustering' to test!")
        else:
            messagebox.showwarning("Demo Not Found", 
                                 "demo_photos folder not found!\n"
                                 "Run create_demo.py first.")
            
    def start_sorting(self):
        # Always check folders first, with clear error messages
        source = self.source_folder.get().strip()
        dest = self.destination_folder.get().strip()
        
        if not source and not dest:
            messagebox.showerror("Folders Not Selected", 
                               "NO FOLDERS SELECTED!\n\n"
                               "Please:\n"
                               "1. Click 'Browse' (green) to select photos folder\n"
                               "2. Click 'Browse' (blue) to select destination folder\n"
                               "3. Or click 'Use Demo' for quick testing")
            return
            
        if not source:
            messagebox.showerror("Source Folder Not Selected", 
                               "SOURCE FOLDER NOT SELECTED!\n\n"
                               "Click the green 'Browse' button to select folder containing photos.")
            return
            
        if not dest:
            messagebox.showerror("Destination Folder Not Selected", 
                               "DESTINATION FOLDER NOT SELECTED!\n\n"
                               "Click the blue 'Browse' button to select folder for results.")
            return
            
        if not os.path.exists(source):
            messagebox.showerror("Source Folder Not Found", 
                               f"SOURCE FOLDER NOT FOUND!\n\n"
                               f"Path: {source}\n\n"
                               "Please ensure the selected folder exists.")
            return
            
        # Check if source has images
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        try:
            image_files = [f for f in os.listdir(source) 
                          if f.lower().endswith(image_extensions)]
            if not image_files:
                messagebox.showwarning("No Photos Found", 
                                     f"NO PHOTOS FOUND!\n\n"
                                     f"Folder: {source}\n\n"
                                     "Please ensure folder contains image files (.jpg, .png, etc.)")
                return
                
            # Show confirmation
            confirm = messagebox.askyesno("Confirm Start", 
                                        f"READY TO START AUTO CLUSTERING?\n\n"
                                        f"Source: {os.path.basename(source)}\n"
                                        f"Destination: {os.path.basename(dest)}\n"
                                        f"Total photos: {len(image_files)}\n\n"
                                        f"Processing will start now!")
            if not confirm:
                return
                
        except Exception as e:
            messagebox.showerror("Error", f"Error checking folder: {str(e)}")
            return
        
        # Start processing
        self.processing = True
        self.start_button.config(state='disabled', text="Processing...")
        self.stop_button.config(state='normal')
        self.progress_var.set(0)
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.log_message("=== STARTING AUTO CLUSTERING PROCESS ===")
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_photos)
        thread.daemon = True
        thread.start()
        
    def stop_sorting(self):
        self.processing = False
        self.start_button.config(state='normal', text="Start Auto Clustering")
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Ready to process photos")
        self.log_message("Process stopped by user")
        
    def detect_faces(self, image_path):
        """Enhanced face detection with multiple cascade classifiers and feature extraction"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return []
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply histogram equalization for better contrast
            gray = cv2.equalizeHist(gray)
            
            # Use multiple detection scales for better accuracy
            faces = []
            
            # Primary detection with strict parameters
            faces_strict = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,  # More precise scaling
                minNeighbors=8,    # Higher confidence threshold
                minSize=(self.min_face_size.get(), self.min_face_size.get()),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # Secondary detection with relaxed parameters for missed faces
            faces_relaxed = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(max(30, self.min_face_size.get()-20), max(30, self.min_face_size.get()-20)),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # Combine and filter overlapping detections
            all_faces = list(faces_strict) + list(faces_relaxed)
            faces = self._filter_overlapping_faces(all_faces)
            
            face_data = []
            for i, (x, y, w, h) in enumerate(faces):
                # Extract face region with padding for better feature extraction
                padding = int(min(w, h) * 0.1)
                x_pad = max(0, x - padding)
                y_pad = max(0, y - padding)
                w_pad = min(gray.shape[1] - x_pad, w + 2*padding)
                h_pad = min(gray.shape[0] - y_pad, h + 2*padding)
                
                face_roi = gray[y_pad:y_pad+h_pad, x_pad:x_pad+w_pad]
                
                # Resize to standard size for comparison
                face_resized = cv2.resize(face_roi, (150, 150))  # Larger size for better features
                
                # Enhanced feature extraction
                features = self._extract_enhanced_features(face_resized)
                
                face_data.append({
                    'features': features,
                    'position': (x, y, w, h),
                    'face_image': face_resized,
                    'quality_score': self._calculate_face_quality(face_resized)
                })
            
            # Sort by quality score (best faces first)
            face_data.sort(key=lambda x: x['quality_score'], reverse=True)
            
            return face_data
            
        except Exception as e:
            self.log_message(f"Error detecting faces in {os.path.basename(image_path)}: {str(e)}")
            return []
    
    def _filter_overlapping_faces(self, faces):
        """Remove overlapping face detections"""
        if len(faces) == 0:
            return []
        
        faces = np.array(faces)
        x1 = faces[:, 0]
        y1 = faces[:, 1]
        x2 = faces[:, 0] + faces[:, 2]
        y2 = faces[:, 1] + faces[:, 3]
        areas = faces[:, 2] * faces[:, 3]
        
        indices = np.argsort(areas)[::-1]  # Sort by area (largest first)
        keep = []
        
        while len(indices) > 0:
            current = indices[0]
            keep.append(current)
            
            # Calculate IoU with remaining faces
            xx1 = np.maximum(x1[current], x1[indices[1:]])
            yy1 = np.maximum(y1[current], y1[indices[1:]])
            xx2 = np.minimum(x2[current], x2[indices[1:]])
            yy2 = np.minimum(y2[current], y2[indices[1:]])
            
            w = np.maximum(0, xx2 - xx1)
            h = np.maximum(0, yy2 - yy1)
            
            intersection = w * h
            union = areas[current] + areas[indices[1:]] - intersection
            iou = intersection / union
            
            # Keep faces with IoU < 0.3 (less overlap)
            indices = indices[1:][iou < 0.3]
        
        return faces[keep].tolist()
    
    def _extract_enhanced_features(self, face_image):
        """Ultra-advanced multi-modal feature extraction for maximum AI accuracy"""
        features = []
        
        try:
            # 1. Enhanced histogram features with multiple bins for precision
            hist_coarse = cv2.calcHist([face_image], [0], None, [32], [0, 256])
            hist_fine = cv2.calcHist([face_image], [0], None, [64], [0, 256])
            hist_coarse_norm = cv2.normalize(hist_coarse, hist_coarse).flatten()
            hist_fine_norm = cv2.normalize(hist_fine, hist_fine).flatten()
            features.extend(hist_coarse_norm)
            features.extend(hist_fine_norm[:32])  # Take first 32 for balance
            
            # 2. Advanced Local Binary Pattern with multiple scales
            try:
                from skimage.feature import local_binary_pattern
                # Multi-scale LBP for enhanced texture analysis
                lbp_8_1 = local_binary_pattern(face_image, 8, 1, method='uniform')
                lbp_16_2 = local_binary_pattern(face_image, 16, 2, method='uniform')
                
                lbp_hist_1, _ = np.histogram(lbp_8_1.ravel(), bins=10, range=(0, 10), density=True)
                lbp_hist_2, _ = np.histogram(lbp_16_2.ravel(), bins=18, range=(0, 18), density=True)
                
                features.extend(lbp_hist_1)
                features.extend(lbp_hist_2)
            except ImportError:
                # Advanced fallback: Multi-directional gradient patterns
                kernels = [
                    np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),  # Horizontal
                    np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),  # Vertical
                    np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]),  # Diagonal 1
                    np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])   # Diagonal 2
                ]
                
                for kernel in kernels:
                    gradient = cv2.filter2D(face_image, cv2.CV_32F, kernel)
                    grad_hist, _ = np.histogram(gradient.ravel(), bins=16, density=True)
                    features.extend(grad_hist)
            
            # 3. Enhanced gradient magnitude and orientation features
            grad_x = cv2.Sobel(face_image, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(face_image, cv2.CV_64F, 0, 1, ksize=3)
            magnitude = np.sqrt(grad_x**2 + grad_y**2)
            orientation = np.arctan2(grad_y, grad_x)
            
            # Magnitude histogram
            mag_hist, _ = np.histogram(magnitude.ravel(), bins=24, density=True)
            features.extend(mag_hist)
            
            # Orientation histogram
            orient_hist, _ = np.histogram(orientation.ravel(), bins=16, range=(-np.pi, np.pi), density=True)
            features.extend(orient_hist)
            
            # 4. Advanced HOG features with multiple configurations
            try:
                from skimage.feature import hog
                # Multiple HOG configurations for comprehensive feature capture
                hog_features_1 = hog(face_image, orientations=9, pixels_per_cell=(8, 8),
                                   cells_per_block=(2, 2), block_norm='L2-Hys')
                hog_features_2 = hog(face_image, orientations=12, pixels_per_cell=(6, 6),
                                   cells_per_block=(3, 3), block_norm='L1')
                
                features.extend(hog_features_1[:60])  # First 60 features
                features.extend(hog_features_2[:40])  # First 40 features
            except ImportError:
                # Enhanced fallback: Multi-scale edge analysis
                for scale in [3, 5, 7]:
                    edges = cv2.Canny(face_image, 50, 150, apertureSize=scale)
                    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
                    features.append(edge_density)
                
                # Add orientation analysis
                angles = np.arctan2(grad_y, grad_x)
                for i in range(8):  # 8 orientation bins
                    angle_range = (-np.pi + i * np.pi/4, -np.pi + (i+1) * np.pi/4)
                    mask = (angles >= angle_range[0]) & (angles < angle_range[1])
                    features.append(np.mean(magnitude[mask]) if np.any(mask) else 0)
            
            # 5. Enhanced spatial analysis with overlapping regions
            h, w = face_image.shape
            
            # Traditional 3x3 grid
            for i in range(3):
                for j in range(3):
                    region = face_image[i*h//3:(i+1)*h//3, j*w//3:(j+1)*w//3]
                    features.append(region.mean())
                    features.append(region.std())
            
            # Additional 2x2 overlapping grid for fine details
            for i in range(2):
                for j in range(2):
                    region = face_image[i*h//4:(i+3)*h//4, j*w//4:(j+3)*w//4]
                    features.append(region.mean())
            
            # 6. Advanced symmetry and structural features
            # Horizontal symmetry analysis
            left_half = face_image[:, :w//2]
            right_half = cv2.flip(face_image[:, w//2:], 1)
            if left_half.shape == right_half.shape:
                symmetry_corr = cv2.matchTemplate(left_half, right_half, cv2.TM_CCOEFF_NORMED)[0][0]
                features.append(max(0, symmetry_corr))
            else:
                features.append(0)
            
            # Vertical structural analysis
            upper_half = face_image[:h//2, :]
            lower_half = face_image[h//2:, :]
            features.append(upper_half.mean())
            features.append(lower_half.mean())
            features.append(abs(upper_half.mean() - lower_half.mean()))
            
            return np.array(features, dtype=np.float32)
            
        except Exception as e:
            # Robust fallback feature extraction
            try:
                hist = cv2.calcHist([face_image], [0], None, [32], [0, 256])
                hist_norm = cv2.normalize(hist, hist).flatten()
                
                grad_x = cv2.Sobel(face_image, cv2.CV_64F, 1, 0, ksize=3)
                grad_y = cv2.Sobel(face_image, cv2.CV_64F, 0, 1, ksize=3)
                gradient_features = [np.mean(grad_x), np.std(grad_x), np.mean(grad_y), np.std(grad_y)]
                
                spatial_features = [face_image.mean(), face_image.std()]
                
                return np.array(list(hist_norm) + gradient_features + spatial_features, dtype=np.float32)
            except:
                # Ultimate fallback
                return np.array([face_image.mean(), face_image.std(), np.sum(face_image)], dtype=np.float32)
    
    def _calculate_face_quality(self, face_image):
        """Ultra-advanced face quality assessment for maximum accuracy"""
        try:
            # Multiple quality metrics for comprehensive assessment
            quality_score = 0.0
            
            # 1. Enhanced sharpness assessment using Laplacian variance
            laplacian = cv2.Laplacian(face_image, cv2.CV_64F)
            sharpness = laplacian.var()
            sharpness_score = min(1.0, sharpness / 1000)  # Enhanced normalization
            quality_score += sharpness_score * 0.3
            
            # 2. Advanced contrast assessment
            hist = cv2.calcHist([face_image], [0], None, [256], [0, 256])
            hist_norm = hist.ravel() / hist.max()
            contrast = np.std(hist_norm)
            contrast_score = min(1.0, contrast * 2)
            quality_score += contrast_score * 0.25
            
            # 3. Optimal brightness balance assessment
            mean_brightness = np.mean(face_image)
            brightness_score = 1.0 - abs(mean_brightness - 127) / 127
            quality_score += brightness_score * 0.2
            
            # 4. Texture richness using gradient analysis
            sobel_x = cv2.Sobel(face_image, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(face_image, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
            texture_score = min(1.0, np.mean(gradient_magnitude) / 50)
            quality_score += texture_score * 0.15
            
            # 5. Face symmetry assessment for enhanced accuracy
            h, w = face_image.shape
            left_half = face_image[:, :w//2]
            right_half_flipped = cv2.flip(face_image[:, w//2:], 1)
            if left_half.shape == right_half_flipped.shape:
                symmetry = cv2.matchTemplate(left_half, right_half_flipped, cv2.TM_CCOEFF_NORMED)[0][0]
                symmetry_score = max(0, symmetry)
                quality_score += symmetry_score * 0.1
            
            return min(1.0, max(0.1, quality_score))
            
        except Exception as e:
            # Robust fallback quality assessment
            try:
                laplacian_var = cv2.Laplacian(face_image, cv2.CV_64F).var()
                return max(0.1, min(1.0, laplacian_var / 1000))
            except:
                return 0.5  # Safe default
            
    def calculate_face_similarity(self, features1, features2):
        """Ultra-advanced multi-metric similarity calculation for maximum AI accuracy"""
        try:
            if len(features1) != len(features2):
                return 0.0
            
            # Handle zero vectors
            norm1 = np.linalg.norm(features1)
            norm2 = np.linalg.norm(features2)
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Advanced normalization strategies
            # 1. L2 normalization
            features1_l2 = features1 / (norm1 + 1e-8)
            features2_l2 = features2 / (norm2 + 1e-8)
            
            # 2. Z-score normalization for robustness
            features1_z = (features1 - np.mean(features1)) / (np.std(features1) + 1e-8)
            features2_z = (features2 - np.mean(features2)) / (np.std(features2) + 1e-8)
            
            # Multiple advanced similarity metrics
            similarities = []
            
            # 1. Enhanced Cosine similarity (most reliable for face features)
            cosine_sim = np.dot(features1_l2, features2_l2)
            similarities.append(('cosine', max(0, cosine_sim), 0.35))
            
            # 2. Pearson correlation coefficient (captures linear relationships)
            try:
                correlation = np.corrcoef(features1, features2)[0, 1]
                if not np.isnan(correlation):
                    similarities.append(('correlation', abs(correlation), 0.25))
                else:
                    similarities.append(('correlation', 0.0, 0.25))
            except:
                similarities.append(('correlation', 0.0, 0.25))
            
            # 3. Inverted Euclidean distance (geometric similarity)
            euclidean_dist = np.linalg.norm(features1_l2 - features2_l2)
            euclidean_sim = 1.0 / (1.0 + euclidean_dist)
            similarities.append(('euclidean', euclidean_sim, 0.20))
            
            # 4. Manhattan distance similarity (L1 norm)
            manhattan_dist = np.sum(np.abs(features1_l2 - features2_l2))
            manhattan_sim = 1.0 / (1.0 + manhattan_dist)
            similarities.append(('manhattan', manhattan_sim, 0.10))
            
            # 5. Chi-squared similarity for histogram features
            try:
                # Apply to positive features (histogram-like)
                pos_feat1 = features1 + abs(np.min(features1)) + 1e-8
                pos_feat2 = features2 + abs(np.min(features2)) + 1e-8
                chi_squared = np.sum((pos_feat1 - pos_feat2)**2 / (pos_feat1 + pos_feat2))
                chi_sim = 1.0 / (1.0 + chi_squared)
                similarities.append(('chi_squared', chi_sim, 0.10))
            except:
                similarities.append(('chi_squared', 0.0, 0.10))
            
            # Weighted combination with quality assessment
            total_weight = 0
            weighted_similarity = 0
            
            for metric_name, similarity_value, weight in similarities:
                # Quality-based weight adjustment
                if similarity_value > 0.8:  # High confidence
                    adjusted_weight = weight * 1.2
                elif similarity_value < 0.3:  # Low confidence
                    adjusted_weight = weight * 0.8
                else:
                    adjusted_weight = weight
                
                weighted_similarity += similarity_value * adjusted_weight
                total_weight += adjusted_weight
            
            final_similarity = weighted_similarity / total_weight if total_weight > 0 else 0.0
            
            # Apply sigmoid smoothing for better discrimination
            final_similarity = 1.0 / (1.0 + np.exp(-10 * (final_similarity - 0.5)))
            
            return max(0.0, min(1.0, final_similarity))
            
        except Exception as e:
            # Robust fallback similarity calculation
            try:
                # Simple cosine similarity as fallback
                norm1 = np.linalg.norm(features1)
                norm2 = np.linalg.norm(features2)
                if norm1 > 0 and norm2 > 0:
                    return max(0.0, np.dot(features1, features2) / (norm1 * norm2))
                else:
                    return 0.0
            except:
                return 0.0
            
    def cluster_faces(self, all_faces_data):
        """Enhanced clustering with hierarchical approach and quality filtering"""
        if not all_faces_data:
            return []
            
        self.log_message(f"HFZRFA Enhanced Clustering: Processing {len(all_faces_data)} faces...")
        
        # Filter out low quality faces
        quality_threshold = np.percentile([face['quality_score'] for face in all_faces_data], 30)
        high_quality_faces = [i for i, face in enumerate(all_faces_data) 
                             if face['quality_score'] >= quality_threshold]
        
        self.log_message(f"Selected {len(high_quality_faces)} high-quality faces for clustering")
        
        # Calculate enhanced similarity matrix
        n_faces = len(all_faces_data)
        similarities = np.zeros((n_faces, n_faces))
        
        for i in range(n_faces):
            for j in range(i, n_faces):
                if i == j:
                    similarities[i][j] = 1.0
                else:
                    sim = self.calculate_face_similarity(
                        all_faces_data[i]['features'], 
                        all_faces_data[j]['features']
                    )
                    similarities[i][j] = sim
                    similarities[j][i] = sim
        
        # Enhanced hierarchical clustering
        threshold = 0.7 - (self.cluster_threshold.get() * 0.5)  # Dynamic threshold
        clusters = [-1] * n_faces
        current_cluster = 0
        
        # Use high-quality faces as cluster seeds
        processed = set()
        
        for seed_idx in high_quality_faces:
            if seed_idx in processed:
                continue
                
            # Start new cluster with this seed
            cluster_members = [seed_idx]
            processed.add(seed_idx)
            clusters[seed_idx] = current_cluster
            
            # Find all faces similar to cluster members
            changed = True
            while changed:
                changed = False
                for candidate_idx in range(n_faces):
                    if candidate_idx in processed:
                        continue
                    
                    # Check similarity to cluster members
                    max_similarity = 0
                    for member_idx in cluster_members:
                        sim = similarities[member_idx][candidate_idx]
                        max_similarity = max(max_similarity, sim)
                    
                    # Add to cluster if similar enough
                    if max_similarity >= threshold:
                        cluster_members.append(candidate_idx)
                        processed.add(candidate_idx)
                        clusters[candidate_idx] = current_cluster
                        changed = True
            
            # Only create cluster if it has multiple members or high-quality single face
            if len(cluster_members) > 1 or all_faces_data[seed_idx]['quality_score'] > quality_threshold * 1.5:
                current_cluster += 1
            else:
                # Remove single low-quality faces from clustering
                for member_idx in cluster_members:
                    clusters[member_idx] = -1
                    processed.remove(member_idx)
        
        # Handle remaining unprocessed faces
        for i in range(n_faces):
            if i not in processed:
                clusters[i] = -1  # Mark as unknown/unique
        
        unique_clusters = len(set(c for c in clusters if c != -1))
        self.log_message(f"HFZRFA Clustering Result: {unique_clusters} distinct person groups identified")
        
        return clusters
        
    def process_photos(self):
        try:
            source_dir = self.source_folder.get()
            dest_dir = self.destination_folder.get()
            
            # Clear previous data
            self.all_face_data = []
            
            # Ensure destination folder exists
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
                self.log_message(f"Created destination folder: {dest_dir}")
                
            # Get all image files
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
            image_files = [f for f in os.listdir(source_dir) 
                          if f.lower().endswith(image_extensions)]
            
            if not image_files:
                self.log_message("No image files found in source folder!")
                self.stop_sorting()
                return
                
            self.log_message(f"Total photos to process: {len(image_files)}")
            self.log_message(f"Auto Clustering mode: {'ON' if self.auto_cluster.get() else 'OFF'}")
            self.log_message(f"Clustering sensitivity: {self.cluster_threshold.get()}")
            self.log_message(f"Minimum face size: {self.min_face_size.get()}px")
            self.log_message("-" * 60)
            
            if self.auto_cluster.get():
                self.process_with_clustering(source_dir, dest_dir, image_files)
            else:
                self.process_simple_grouping(source_dir, dest_dir, image_files)
                
        except Exception as e:
            self.log_message(f"Major error: {str(e)}")
            self.stop_sorting()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def process_with_clustering(self, source_dir, dest_dir, image_files):
        """Process with intelligent face clustering"""
        self.log_message("PHASE 1: Detecting and analyzing all faces...")
        
        processed_count = 0
        face_found_count = 0
        total_faces = 0
        
        # Phase 1: Extract all faces and their features
        for i, image_file in enumerate(image_files):
            if not self.processing:
                break
                
            try:
                progress = (i / len(image_files)) * 40  # 40% for face detection
                self.progress_var.set(progress)
                self.status_label.config(text=f"Analyzing faces: {image_file}")
                
                image_path = os.path.join(source_dir, image_file)
                self.log_message(f"Analyzing: {image_file}")
                
                faces_data = self.detect_faces(image_path)
                
                if faces_data:
                    face_found_count += 1
                    for j, face_data in enumerate(faces_data):
                        self.all_face_data.append({
                            'file': image_file,
                            'face_index': j,
                            'total_faces': len(faces_data),
                            'features': face_data['features'],
                            'position': face_data['position']
                        })
                        total_faces += 1
                    
                    self.log_message(f"   Found {len(faces_data)} faces")
                else:
                    # Copy to no face folder
                    no_face_folder = os.path.join(dest_dir, "No_Face_Detected")
                    if not os.path.exists(no_face_folder):
                        os.makedirs(no_face_folder)
                    copyfile(image_path, os.path.join(no_face_folder, image_file))
                    self.log_message(f"   No faces detected")
                
                processed_count += 1
                
            except Exception as e:
                self.log_message(f"   Error: {str(e)}")
        
        if not self.all_face_data:
            self.log_message("No faces were successfully analyzed!")
            self.stop_sorting()
            return
            
        self.log_message(f"PHASE 1 Complete: {total_faces} faces analyzed from {face_found_count} photos")
        self.log_message("-" * 60)
        
        # Phase 2: Cluster faces
        self.progress_var.set(50)
        self.status_label.config(text="Clustering similar faces...")
        self.log_message("PHASE 2: Clustering similar faces...")
        
        clusters = self.cluster_faces(self.all_face_data)
        unique_clusters = len(set(clusters))
        
        self.log_message("-" * 60)
        
        # Phase 3: Sort photos with clean organization
        self.log_message("PHASE 3: Organizing photos with HFZRFA precision...")
        cluster_stats = defaultdict(int)
        processed_files = set()  # Track processed files to avoid duplicates
        
        # Group faces by image file first
        files_by_image = defaultdict(list)
        for i, face_data in enumerate(self.all_face_data):
            files_by_image[face_data['file']].append((i, clusters[i]))
        
        for image_file, face_list in files_by_image.items():
            if not self.processing:
                break
            
            try:
                if image_file in processed_files:
                    continue
                
                progress = 60 + (len(processed_files) / len(files_by_image)) * 40
                self.progress_var.set(progress)
                self.status_label.config(text=f"Organizing: {image_file}")
                
                source_path = os.path.join(source_dir, image_file)
                
                # Determine the primary person in the image
                cluster_counts = defaultdict(int)
                for _, cluster_id in face_list:
                    if cluster_id != -1:
                        cluster_counts[cluster_id] += 1
                
                if cluster_counts:
                    # Use the most frequent cluster (primary person)
                    primary_cluster = max(cluster_counts.items(), key=lambda x: x[1])[0]
                    folder_name = f"Person_{primary_cluster + 1:02d}"
                else:
                    # No recognizable faces
                    folder_name = "Unknown_Faces"
                
                # Create destination folder
                person_folder = os.path.join(dest_dir, folder_name)
                if not os.path.exists(person_folder):
                    os.makedirs(person_folder)
                
                # Copy the original image (no duplicates)
                destination_path = os.path.join(person_folder, image_file)
                if not os.path.exists(destination_path):
                    copyfile(source_path, destination_path)
                    cluster_stats[folder_name] += 1
                
                processed_files.add(image_file)
                
            except Exception as e:
                self.log_message(f"   Error organizing {image_file}: {str(e)}")
        
        # Final results
        self.progress_var.set(100)
        self.status_label.config(text="HFZRFA Auto Clustering completed successfully!")
        self.log_message("=" * 60)
        self.log_message("HFZRFA AUTO CLUSTERING PROCESS COMPLETED!")
        self.log_message(f"ENHANCED STATISTICS:")
        self.log_message(f"   • Total photos processed: {processed_count}")
        self.log_message(f"   • Photos with faces: {face_found_count}")
        self.log_message(f"   • Total faces analyzed: {total_faces}")
        self.log_message(f"   • Distinct person groups: {unique_clusters}")
        self.log_message(f"   • Photos without faces: {processed_count - face_found_count}")
        
        self.log_message("CLEAN ORGANIZATION RESULTS:")
        for folder_name, count in sorted(cluster_stats.items()):
            self.log_message(f"   • {folder_name}: {count} photos")
            
        self.log_message(f"Results saved to: {dest_dir}")
        self.log_message("© 2025 HFZRFA - Advanced AI Photo Organization")
        self.log_message("=" * 60)
        
        # Reset button states
        self.processing = False
        self.start_button.config(state='normal', text="Start Auto Clustering")
        self.stop_button.config(state='disabled')
        
        # Show results
        summary = (f"HFZRFA Auto Clustering Completed!\n\n"
                  f"ENHANCED RESULTS:\n"
                  f"• Total photos: {processed_count}\n"
                  f"• Photos with faces: {face_found_count}\n"
                  f"• Total faces: {total_faces}\n"
                  f"• Distinct persons: {unique_clusters}\n\n"
                  f"Clean organization saved to:\n{dest_dir}\n\n"
                  f"© 2025 HFZRFA Technology")
        
        messagebox.showinfo("HFZRFA Auto Clustering Complete", summary)
        
        if messagebox.askyesno("Open Results", "Would you like to open the organized results folder?"):
            os.startfile(dest_dir)
            
    def process_simple_grouping(self, source_dir, dest_dir, image_files):
        """Simple grouping by face count"""
        processed_count = 0
        face_found_count = 0
        stats = defaultdict(int)
        
        for i, image_file in enumerate(image_files):
            if not self.processing:
                break
                
            try:
                progress = (i / len(image_files)) * 100
                self.progress_var.set(progress)
                self.status_label.config(text=f"Memproses: {image_file}")
                
                image_path = os.path.join(source_dir, image_file)
                faces_data = self.detect_faces(image_path)
                face_count = len(faces_data)
                
                if face_count == 0:
                    folder_name = "No_Face_Detected"
                    stats['no_face'] += 1
                elif face_count == 1:
                    folder_name = "Single_Face" if self.group_by_faces.get() else "With_Faces"
                    stats['single'] += 1
                    face_found_count += 1
                else:
                    folder_name = f"Multiple_Faces_{face_count}" if self.group_by_faces.get() else "With_Faces"
                    stats['multiple'] += 1
                    face_found_count += 1
                
                # Create and copy
                dest_folder = os.path.join(dest_dir, folder_name)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                copyfile(image_path, os.path.join(dest_folder, image_file))
                processed_count += 1
                
                self.log_message(f"✓ {image_file}: {face_count} faces -> {folder_name}")
                
            except Exception as e:
                self.log_message(f"Error: {str(e)}")
        
        # Results
        self.progress_var.set(100)
        self.status_label.config(text="Completed!")
        self.log_message("PROCESS COMPLETED!")
        
        # Reset button states
        self.processing = False
        self.start_button.config(state='normal', text="Start Auto Clustering")
        self.stop_button.config(state='disabled')

def main():
    try:
        cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        root = tk.Tk()
        app = PhotoSorterAdvanced(root)
        
        # Center window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        root.mainloop()
        
    except ImportError as e:
        print("Error: OpenCV not found!")
        print("Install with: pip install opencv-python")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
