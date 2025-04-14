#!/usr/bin/env python3
"""
Deepfake Detection Inference Server
-----------------------------------
This server loads a deepfake detection model and provides an API endpoint
for analyzing images to detect potential deepfakes.
"""

import os
import uuid
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import base64

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables
model = None
temp_dir = "temp_uploads"

# Create temp directory if it doesn't exist
os.makedirs(temp_dir, exist_ok=True)

def load_model():
    """Load the deepfake detection model"""
    global model
    if model is None:
        print("Loading deepfake detection model...")
        try:
            # Load the model with CPU support
            model = pipeline('image-classification', model="prithivMLmods/AI-vs-Deepfake-vs-Real", device=-1)
            print("Model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    return True

def analyze_image(image_data):
    """
    Analyze an image to detect deepfakes
    
    Args:
        image_data: The image data as numpy array
        
    Returns:
        dict: Analysis results with scores for each category
    """
    global model
    
    if model is None:
        return {"error": "Model not loaded"}
    
    try:
        # Save image to temporary file (required by the model)
        temp_filename = os.path.join(temp_dir, f"temp_frame_{uuid.uuid4()}.jpg")
        cv2.imwrite(temp_filename, image_data)
        
        # Run inference on the image
        result = model(temp_filename)
        
        # Clean up temporary file
        try:
            os.remove(temp_filename)
        except:
            pass
        
        # Format the results
        formatted_results = {}
        for item in result:
            label = item['label']
            score = item['score']
            formatted_results[label] = float(score)
        
        return formatted_results
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if model is not None:
        return jsonify({"status": "healthy", "model_loaded": True})
    else:
        return jsonify({"status": "unhealthy", "model_loaded": False})

@app.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze an image for deepfakes"""
    if not load_model():
        return jsonify({"error": "Failed to load model"}), 500
    
    if 'image' not in request.json:
        return jsonify({"error": "No image data provided"}), 400
    
    try:
        # Decode base64 image
        image_data = request.json['image']
        image_bytes = base64.b64decode(image_data)
        
        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400
        
        # Analyze the image
        results = analyze_image(image)
        
        if "error" in results:
            return jsonify(results), 500
        
        return jsonify({
            "success": True,
            "results": results
        })
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    # Load model at startup
    load_model()
    
    # Run the server
    # Get port from environment variable, default to 8080 to match CVM upstream-port
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
