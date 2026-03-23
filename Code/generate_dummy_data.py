import cv2
import numpy as np
import pickle
import os
import random

# Create gestures directory
if not os.path.exists("gestures"):
    os.mkdir("gestures")

# Generate dummy gesture images
image_x, image_y = 50, 50
num_gestures = 5
images_per_gesture = 1200

print("Generating dummy gesture images...")

for gesture_id in range(1, num_gestures + 1):
    gesture_folder = f"gestures/{gesture_id}"
    if not os.path.exists(gesture_folder):
        os.mkdir(gesture_folder)
    
    for img_num in range(1, images_per_gesture + 1):
        # Create synthetic grayscale images
        # Simulate hand/gesture images with random patterns
        img = np.random.randint(50, 200, (image_x, image_y), dtype=np.uint8)
        
        # Add some structure to make it more realistic
        center_x, center_y = random.randint(10, 40), random.randint(10, 40)
        radius = random.randint(5, 15)
        
        # Draw a circle to simulate hand blob
        cv2.circle(img, (center_x, center_y), radius, 200, -1)
        
        # Add some noise
        noise = np.random.randint(0, 50, (image_x, image_y), dtype=np.uint8)
        img = cv2.addWeighted(img, 0.7, noise, 0.3, 0)
        
        # Save image
        cv2.imwrite(f"{gesture_folder}/{img_num}.jpg", img)
        
        if img_num % 200 == 0:
            print(f"  Gesture {gesture_id}: {img_num}/{images_per_gesture}")

print("✓ Dummy images generated!")

# Create hand histogram (dummy)
print("Creating hand histogram...")
hist = np.random.randint(0, 255, (180, 256), dtype=np.uint8)
with open("hist", "wb") as f:
    pickle.dump(hist, f)
print("✓ Hand histogram created!")

print("\nDummy data generation complete!")
print(f"Generated {num_gestures} gestures with {images_per_gesture} images each")
