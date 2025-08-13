import os
import io
import base64
import requests
from flask import Blueprint, request, jsonify
from PIL import Image
from flask_cors import cross_origin

ghibli_bp = Blueprint('ghibli', __name__)

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"
HF_TOKEN = os.getenv('HUGGINGFACE_TOKEN')  # You'll need to set this environment variable

def query_huggingface(image_data):
    """Query Hugging Face API for Ghibli style conversion"""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        print(f"Calling Hugging Face API: {HF_API_URL}")
        
        # InstructPix2Pix expects a JSON payload with image and instruction
        # Convert image to base64 for JSON payload
        import base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        payload = {
            "inputs": {
                "image": f"data:image/jpeg;base64,{image_base64}",
                "instruction": "Convert this image to Studio Ghibli anime style with beautiful colors and detailed artwork"
            }
        }
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)
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
    print("=== Starting image conversion ===")
    print(f"HF_TOKEN available: {bool(HF_TOKEN)}")
    print(f"HF_TOKEN length: {len(HF_TOKEN) if HF_TOKEN else 0}")
    
    try:
        # Check if Hugging Face token is available
        if not HF_TOKEN:
            print("ERROR: HUGGINGFACE_TOKEN not set")
            return jsonify({'error': 'Hugging Face API token not configured'}), 500
        
        # Check if image file is present
        if 'image' not in request.files:
            print("ERROR: No image file in request.files")
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            print("ERROR: Empty filename")
            return jsonify({'error': 'No image file selected'}), 400
        
        # Read and process the image
        image_data = file.read()
        print(f"Processing image: {file.filename}, size: {len(image_data)} bytes")
        
        # Call Hugging Face API
        print("About to call Hugging Face API...")
        converted_image_data = query_huggingface(image_data)
        
        if converted_image_data:
            print(f"Success! Converted image size: {len(converted_image_data)} bytes")
            base64_image = base64.b64encode(converted_image_data).decode("utf-8")
            return jsonify({
                "success": True,
                "message": "Image converted to Ghibli style successfully!",
                "converted_image": f"data:image/png;base64,{base64_image}"
            })
        else:
            print("ERROR: Hugging Face API returned None")
            return jsonify({"error": "Failed to convert image using Hugging Face API. Check backend logs for details."}), 500
        
    except Exception as e:
        print(f"EXCEPTION in convert_to_ghibli: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

@ghibli_bp.route("/health", methods=["GET"])
@cross_origin()
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "service": "Ghibli Image Converter",
        "hf_token_available": bool(HF_TOKEN),
        "hf_token_length": len(HF_TOKEN) if HF_TOKEN else 0
    })

@ghibli_bp.route("/test-hf", methods=["GET"])
@cross_origin()
def test_huggingface():
    """Test Hugging Face API connection"""
    try:
        if not HF_TOKEN:
            return jsonify({"error": "Hugging Face token not configured"}), 500
        
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        response = requests.get("https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix", headers=headers, timeout=10)
        
        return jsonify({
            "status": "success",
            "hf_response_status": response.status_code,
            "hf_response_text": response.text[:200] if response.text else "No response text"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

