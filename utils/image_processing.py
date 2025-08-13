# utils/image_processing.py
import cv2
import numpy as np
from sklearn.cluster import KMeans

def get_dominant_colors(image_path, n_colors=5):
    """Get dominant hex colors from an image"""
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    # Resize for faster processing
    img = cv2.resize(img, (300, 300))
    
    # Convert to RGB and reshape
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1, 3)
    
    # Get dominant colors
    kmeans = KMeans(n_clusters=n_colors, n_init=10)
    kmeans.fit(pixels)
    
    # Convert to hex codes
    hex_codes = []
    for center in kmeans.cluster_centers_:
        rgb = tuple(int(c) for c in center)
        hex_codes.append(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
    
    return hex_codes