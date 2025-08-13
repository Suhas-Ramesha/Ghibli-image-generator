import os
import io
import base64
import requests
from flask import Blueprint, request, jsonify
from PIL import Image
from flask_cors import cross_origin

ghibli_bp = Blueprint('ghibli', __name__)

# Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDjhkmygph3tfuZjcenRKCD0E5RvPGAlsg')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def query_gemini(image_data):
    """Query Gemini API for Ghibli style image generation"""
    try:
        print(f"Calling Gemini API: {GEMINI_API_URL}")
        
        # Convert image to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Prepare the request payload for Gemini
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Generate a Studio Ghibli style anime version of this image. Make it beautiful with vibrant colors, detailed artwork, and the characteristic Ghibli aesthetic. Return only the generated image as base64 data."
                        },
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192
            }
        }
        
        # Make the API request
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        print(f"Gemini API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Successfully received response from Gemini API")
            result = response.json()
            
            # Extract the generated image from the response
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    for part in candidate['content']['parts']:
                        if 'inline_data' in part and part['inline_data']['mime_type'].startswith('image/'):
                            # Decode the base64 image data
                            image_data = base64.b64decode(part['inline_data']['data'])
                            return image_data
            
            print("No image data found in Gemini response")
            return None
        else:
            print(f"Gemini API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("Gemini API request timed out")
        return None
    except Exception as e:
        print(f"Error querying Gemini API: {e}")
        return None

@ghibli_bp.route('/convert', methods=['POST'])
@cross_origin()
def convert_to_ghibli():
    """Convert uploaded image to Ghibli style"""
    print("=== Starting image conversion ===")
    print(f"GEMINI_API_KEY available: {bool(GEMINI_API_KEY)}")
    print(f"GEMINI_API_KEY length: {len(GEMINI_API_KEY) if GEMINI_API_KEY else 0}")
    
    try:
        # Check if Gemini API key is available
        if not GEMINI_API_KEY:
            print("ERROR: GEMINI_API_KEY not set")
            return jsonify({'error': 'Gemini API key not configured'}), 500
        
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
        
        # Call Gemini API
        print("About to call Gemini API...")
        converted_image_data = query_gemini(image_data)
        
        if converted_image_data:
            print(f"Success! Converted image size: {len(converted_image_data)} bytes")
            base64_image = base64.b64encode(converted_image_data).decode("utf-8")
            return jsonify({
                "success": True,
                "message": "Image converted to Ghibli style successfully!",
                "converted_image": f"data:image/png;base64,{base64_image}"
            })
        else:
            print("ERROR: Gemini API returned None")
            return jsonify({"error": "Failed to convert image using Gemini API. Check backend logs for details."}), 500
        
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
        "gemini_api_key_available": bool(GEMINI_API_KEY),
        "gemini_api_key_length": len(GEMINI_API_KEY) if GEMINI_API_KEY else 0
    })

@ghibli_bp.route("/test-gemini", methods=["GET"])
@cross_origin()
def test_gemini():
    """Test Gemini API connection"""
    try:
        if not GEMINI_API_KEY:
            return jsonify({"error": "Gemini API key not configured"}), 500
        
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Hello, this is a test message."
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        return jsonify({
            "status": "success",
            "gemini_response_status": response.status_code,
            "gemini_response_text": response.text[:200] if response.text else "No response text"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

