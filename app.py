# app.py
from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

def process_image(image_data):
    # Convert base64 string to numpy array
    nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Perform object detection using OpenCV
    # Example: Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Convert processed image to base64 string
    retval, buffer = cv2.imencode('.jpg', gray_image)
    processed_image_data = base64.b64encode(buffer).decode('utf-8')
    return processed_image_data

@app.route('/process-image', methods=['POST'])
def process_image_route():
    data = request.json
    image_data = data.get('image')
    processed_image_data = process_image(image_data)
    return jsonify({'processedImage': processed_image_data})

if __name__ == '__main__':
    app.run(debug=True)
