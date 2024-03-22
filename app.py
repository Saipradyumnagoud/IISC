from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# Create upload and processed image directories if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def process_image(image_data):
    # Convert base64 string to numpy array
    nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Resize the image to a specific width and height
    resized_image = cv2.resize(image, (300, 200))  # Example: Resize to 300x200 pixels

    # Save processed image
    processed_image_path = os.path.join(PROCESSED_FOLDER, 'processed_image.jpg')
    cv2.imwrite(processed_image_path, resized_image)

    return processed_image_path

@app.route('/process-image', methods=['POST'])
def process_image_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save uploaded image
    uploaded_image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(uploaded_image_path)

    # Process the uploaded image
    processed_image_path = process_image(image_file.read())

    # Return the URLs of original and processed images
    return jsonify({
        'originalImageUrl': uploaded_image_path,
        'processedImageUrl': processed_image_path
    })

if __name__ == '__main__':
    app.run(debug=True)
