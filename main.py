#!/usr/bin/env python3
"""
AI Photo Sorter with Auto Clustering
Professional entry point for AI photo sorting application

Features:
- Auto clustering: Group same people into separate folders
- Face detection: Automatic face detection with OpenCV
- User-friendly GUI: Easy-to-use interface
- Multiple versions: 3 versions for different needs

Author: AI Assistant
Version: 2.0 (Auto Clustering)
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def main():
    """Main entry point - display version selection"""
    
    # Check if we're in the right directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    # Show version selection dialog
    choice = messagebox.askyesnocancel(
        "AI Photo Sorter - Version Selection",
        "Choose the version you want to run:\n\n"
        "YES: Auto Clustering (RECOMMENDED)\n"
        "   → Group same people automatically\n"
        "   → Result: Person_01/, Person_02/, etc\n\n"
        "NO: OpenCV Simple\n"
        "   → Sort by face count\n"
        "   → Result: Single_Face/, Multiple_Faces/\n\n"
        "CANCEL: Advanced Recognition\n"
        "   → Known faces database + Auto clustering\n"
        "   → Requires face_recognition library"
    )
    
    root.destroy()
    
    if choice is True:
        # Auto Clustering (Recommended)
        print("Launching Auto Clustering version...")
        try:
            subprocess.run([sys.executable, "photo_sorter_advanced.py"], check=True)
        except FileNotFoundError:
            print("Error: photo_sorter_advanced.py not found!")
        except subprocess.CalledProcessError:
            print("Error: Failed to run auto clustering version!")
            
    elif choice is False:
        # OpenCV Simple
        print("Launching OpenCV Simple version...")
        try:
            subprocess.run([sys.executable, "photo_sorter_opencv.py"], check=True)
        except FileNotFoundError:
            print("Error: photo_sorter_opencv.py not found!")
        except subprocess.CalledProcessError:
            print("Error: Failed to run OpenCV simple version!")
            
    elif choice is None:
        # Advanced Recognition
        print("Launching Advanced Recognition version...")
        try:
            subprocess.run([sys.executable, "photo_sorter_gui.py"], check=True)
        except FileNotFoundError:
            print("Error: photo_sorter_gui.py not found!")
        except subprocess.CalledProcessError:
            print("Error: Failed to run advanced recognition version!")
            print("Tip: Make sure face_recognition library is installed")
    
    else:
        print("No version selected. Exiting...")

if __name__ == "__main__":
    print("=" * 50)
    print("AI PHOTO SORTER with AUTO CLUSTERING")
    print("=" * 50)
    print()
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7+ required!")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check required packages
    try:
        import cv2
        import numpy
        import PIL
        print("All required packages are available")
    except ImportError as e:
        print(f"Error: Missing required package - {e}")
        print("Run: pip install opencv-python pillow numpy")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("Starting application launcher...")
    print()
    
    main()
