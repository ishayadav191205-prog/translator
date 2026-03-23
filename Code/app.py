"""
Flask API for Sign Language Interpreter
Provides REST endpoints for gesture prediction
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import base64
import os
import sqlite3
from datetime import datetime

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)  # Enable cross-origin requests

# Load model
print("[INFO] Loading trained model...")
try:
    model = load_model('cnn_model_keras2.h5')
    print("[SUCCESS] Model loaded!")
except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")
    model = None

# Configuration
MODEL_INPUT_SIZE = (50, 50)
CONFIDENCE_THRESHOLD = 0.5

# Model memory (last 10 predictions)
prediction_history = []

def get_gesture_name(gesture_id):
    """Get gesture name from database"""
    try:
        if os.path.exists("gesture_db.db"):
            conn = sqlite3.connect("gesture_db.db")
            cursor = conn.execute(f"SELECT g_name FROM gesture WHERE g_id={gesture_id}")
            result = cursor.fetchone()
            conn.close()
            if result:
                return result[0]
    except Exception as e:
        print(f"[WARNING] Database error: {e}")
    
    return f"Gesture_{gesture_id}"

def process_image(img_base64):
    """Decode and process base64 image"""
    try:
        # Decode base64
        if ',' in img_base64:
            img_base64 = img_base64.split(',')[1]
        
        img_data = base64.b64decode(img_base64)
        img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            return None, "Invalid image format"
        
        # Resize and normalize
        img = cv2.resize(img, MODEL_INPUT_SIZE)
        img = np.array(img, dtype=np.float32) / 255.0
        img = np.reshape(img, (1, MODEL_INPUT_SIZE[0], MODEL_INPUT_SIZE[1], 1))
        
        return img, "Success"
    except Exception as e:
        return None, f"Image processing error: {str(e)}"

def predict_gesture(img_array):
    """Make prediction on processed image"""
    try:
        if model is None:
            return None, None, "Model not loaded"
        
        predictions = model.predict(img_array, verbose=0)[0]
        gesture_id = int(np.argmax(predictions))
        confidence = float(max(predictions)) * 100
        
        return gesture_id, confidence, "Success"
    except Exception as e:
        return None, None, f"Prediction error: {str(e)}"

# ============================================================
# API ENDPOINTS
# ============================================================

@app.route('/')
def index():
    """Serve main HTML page"""
    try:
        return send_from_directory('static', 'index.html')
    except:
        return "Error: static/index.html not found", 404

@app.route('/predict', methods=['POST'])
def predict():
    """
    POST /predict
    Predicts gesture from image
    
    Request body:
    {
        "image": "base64_encoded_jpeg"
    }
    
    Response:
    {
        "status": "success",
        "gesture": 1,
        "gesture_name": "A",
        "confidence": 85.5,
        "all_predictions": [0.1, 0.2, 0.85, 0.05, ...],
        "timestamp": "2026-03-23T14:30:45"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing image data'
            }), 400
        
        img_base64 = data['image']
        
        # Process image
        img_array, msg = process_image(img_base64)
        if img_array is None:
            return jsonify({
                'status': 'error',
                'message': msg
            }), 400
        
        # Make prediction
        gesture_id, confidence, msg = predict_gesture(img_array)
        if gesture_id is None:
            return jsonify({
                'status': 'error',
                'message': msg
            }), 500
        
        gesture_name = get_gesture_name(gesture_id)
        
        # Store in history
        prediction_record = {
            'gesture': gesture_id,
            'gesture_name': gesture_name,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
        prediction_history.append(prediction_record)
        if len(prediction_history) > 10:
            prediction_history.pop(0)
        
        return jsonify({
            'status': 'success',
            'gesture': gesture_id,
            'gesture_name': gesture_name,
            'confidence': round(confidence, 2),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/status', methods=['GET'])
def status():
    """Get API status"""
    return jsonify({
        'status': 'running',
        'model': 'cnn_model_keras2.h5',
        'model_loaded': model is not None,
        'predictions_made': len(prediction_history),
        'history_size': 10,
        'input_shape': (50, 50, 1),
        'confidence_threshold': CONFIDENCE_THRESHOLD
    })

@app.route('/history', methods=['GET'])
def history():
    """Get prediction history"""
    return jsonify({
        'status': 'success',
        'count': len(prediction_history),
        'history': prediction_history
    })

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear prediction history"""
    global prediction_history
    prediction_history = []
    return jsonify({
        'status': 'success',
        'message': 'History cleared'
    })

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SIGN LANGUAGE INTERPRETER - FLASK API SERVER")
    print("="*60)
    print("\n[INFO] Starting Flask server...")
    print("[INFO] Model status:", "✓ Loaded" if model is not None else "✗ Failed")
    print("\n[INFO] API Endpoints:")
    print("  GET  http://localhost:5000/              → Web UI")
    print("  POST http://localhost:5000/predict       → Make prediction")
    print("  GET  http://localhost:5000/health        → Health check")
    print("  GET  http://localhost:5000/status        → API status")
    print("  GET  http://localhost:5000/history       → View predictions")
    print("  POST http://localhost:5000/clear-history → Clear history")
    print("\n[INFO] Server running on: http://localhost:5000")
    print("[INFO] Press CTRL+C to stop\n")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
