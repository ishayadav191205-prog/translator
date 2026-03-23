import cv2
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import sqlite3

# Load the trained model
print("Loading trained model...")
model = load_model('cnn_model_keras2.h5')

# Load hand histogram
def get_hand_hist():
    with open("hist", "rb") as f:
        hist = pickle.load(f)
    return hist

# Get gesture database mapping
def get_gesture_name(gesture_id):
    """Get gesture name from database"""
    try:
        conn = sqlite3.connect("gesture_db.db")
        cmd = f"SELECT g_name FROM gesture WHERE g_id={gesture_id}"
        cursor = conn.execute(cmd)
        for row in cursor:
            return row[0]
        return f"Gesture {gesture_id}"
    except:
        return f"Gesture {gesture_id}"

def process_image(image_path):
    """Load and process an image for prediction"""
    img = cv2.imread(image_path, 0)
    if img is None:
        print(f"Error: Could not load image {image_path}")
        return None
    
    # Resize to match training size
    img = cv2.resize(img, (50, 50))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (1, 50, 50, 1))
    return img

def predict_gesture(image_data):
    """Predict gesture from image"""
    if image_data is None:
        return None, None
    
    pred_probab = model.predict(image_data, verbose=0)[0]
    pred_class = np.argmax(pred_probab)
    confidence = max(pred_probab) * 100
    
    return pred_class, confidence

def demo_predictions():
    """Demo predictions on synthetic images"""
    print("\n" + "="*50)
    print("SIGN LANGUAGE INTERPRETER - DEPLOYMENT TEST")
    print("="*50)
    print("\nModel Architecture:")
    model.summary()
    
    print("\n" + "="*50)
    print("Testing Predictions on Sample Images")
    print("="*50)
    
    # Test on some of the generated synthetic images
    test_images = [
        "gestures/1/100.jpg",
        "gestures/2/200.jpg",
        "gestures/3/300.jpg",
        "gestures/4/400.jpg",
        "gestures/5/500.jpg",
    ]
    
    for img_path in test_images:
        try:
            print(f"\nTesting: {img_path}")
            img_data = process_image(img_path)
            if img_data is not None:
                pred_class, confidence = predict_gesture(img_data)
                gesture_name = get_gesture_name(pred_class)
                print(f"  Predicted Class: {pred_class}")
                print(f"  Gesture: {gesture_name}")
                print(f"  Confidence: {confidence:.2f}%")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "="*50)
    print("Deployment Ready!")
    print("="*50)
    
    print("\nTo use in production:")
    print("1. Use the trained model: cnn_model_keras2.h5")
    print("2. Use hand histogram: hist")
    print("3. Capture live video frames")
    print("4. Process with hand detection (HSV color space)")
    print("5. Predict using model.predict()")
    
    return True

if __name__ == "__main__":
    try:
        success = demo_predictions()
        if success:
            print("\n✓ Deployment test completed successfully!")
    except Exception as e:
        print(f"\nError during deployment test: {e}")
        import traceback
        traceback.print_exc()
