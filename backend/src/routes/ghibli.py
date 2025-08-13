import os
import io
import base64
import requests
from flask import Blueprint, request, jsonify
from PIL import Image
from flask_cors import cross_origin

ghibli_bp = Blueprint('ghibli', __name__)

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/nitrosocke/Ghibli-Diffusion"
HF_TOKEN = os.getenv('HUGGINGFACE_TOKEN')  # You'll need to set this environment variable

def query_huggingface(image_data):
    """Query Hugging Face API for Ghibli style conversion"""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        print(f"Calling Hugging Face API: {HF_API_URL}")
        response = requests.post(HF_API_URL, headers=headers, data=image_data, timeout=60)
        print(f"Hugging Face API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Successfully received converted image from Hugging Face API")
            return response.content
        else:
            print(f"Hugging Face API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("Hugging Face API request timed out")
        return None
    except Exception as e:
        print(f"Error querying Hugging Face: {e}")
        return None

@ghibli_bp.route('/convert', methods=['POST'])
@cross_origin()
def convert_to_ghibli():
    """Convert uploaded image to Ghibli style"""
    try:
        # Check if Hugging Face token is available
        if not HF_TOKEN:
            print("Warning: HUGGINGFACE_TOKEN not set")
            return jsonify({'error': 'Hugging Face API token not configured'}), 500
        
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Read and process the image
        image_data = file.read()
        print(f"Processing image: {file.filename}, size: {len(image_data)} bytes")
        
        # Call Hugging Face API
        converted_image_data = query_huggingface(image_data)
        
        if converted_image_data:
            base64_image = base64.b64encode(converted_image_data).decode("utf-8")
            return jsonify({
                "success": True,
                "message": "Image converted to Ghibli style successfully!",
                "converted_image": f"data:image/png;base64,{base64_image}"
            })
        else:
            return jsonify({"error": "Failed to convert image using Hugging Face API. Check backend logs for details."}), 500
        
    except Exception as e:
        print(f"Error in convert_to_ghibli: {str(e)}")
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

@ghibli_bp.route("/health", methods=["GET"])
@cross_origin()
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Ghibli Image Converter"})

