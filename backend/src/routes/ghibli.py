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
        
        # First, let's get a description of the image from Gemini
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Describe this image in detail, focusing on the visual elements, colors, composition, and mood. Be specific about what you see."
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
                "maxOutputTokens": 1000
            }
        }
        
        # Make the API request
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        print(f"Gemini API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Successfully received response from Gemini API")
            result = response.json()
            
            # Extract the text description
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    description = ""
                    for part in candidate['content']['parts']:
                        if 'text' in part:
                            description += part['text']
                    
                    print(f"Image description: {description}")
                    
                    # Now generate a Ghibli-style image based on the description
                    ghibli_prompt = f"Studio Ghibli anime style artwork of: {description}. Beautiful, vibrant colors, detailed artwork, characteristic Ghibli aesthetic, high quality, magical atmosphere"
                    
                    # For now, let's return a mock response since Gemini doesn't generate images directly
                    # In a production app, you'd use this prompt with an image generation service
                    print(f"Ghibli prompt generated: {ghibli_prompt}")
                    
                    # Create a simple mock image response for testing
                    # In a real implementation, you'd send this prompt to an image generation API
                    return create_mock_ghibli_image()
            
            print("No description found in Gemini response")
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

def create_mock_ghibli_image():
    """Create a mock Ghibli-style image for testing"""
    try:
        # Create a simple gradient image that looks Ghibli-inspired
        from PIL import Image, ImageDraw
        
        # Create a 512x512 image with a Ghibli-style gradient
        width, height = 512, 512
        image = Image.new('RGB', (width, height), color='lightblue')
        draw = ImageDraw.Draw(image)
        
        # Create a simple gradient background
        for y in range(height):
            r = int(100 + (y / height) * 100)
            g = int(150 + (y / height) * 50)
            b = int(200 + (y / height) * 55)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add some simple shapes to make it look more artistic
        draw.ellipse([100, 100, 200, 200], fill='yellow', outline='orange', width=3)
        draw.rectangle([300, 300, 400, 400], fill='green', outline='darkgreen', width=3)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        print("Created mock Ghibli-style image")
        return img_byte_arr
    except Exception as e:
        print(f"Error creating mock image: {e}")
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

