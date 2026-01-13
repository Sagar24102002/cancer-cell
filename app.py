from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import time
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'f:/cancer/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
            
        image = request.files['image']
        
        if image.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if not allowed_file(image.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        # Secure the filename and create save path
        filename = secure_filename(image.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Create directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save original image
        image.save(save_path)
        
        # Process image for model
        try:
            img = Image.open(save_path)
            img = img.convert('RGB')
            img = img.resize((224, 224))
            
            # Save processed image
            processed_filename = f'processed_{filename}'
            processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
            img.save(processed_path)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        # Get form data with default values
        patient_data = {
            'name': request.form.get('name', ''),
            'age': request.form.get('age', ''),
            'sex': request.form.get('sex', ''),
            'email': request.form.get('email', '')
        }

        # Prediction scores
        confidence_scores = {
            'benign': 0.15,
            'malignant': 0.25,
            'normal': 0.60
        }
        
        label = max(confidence_scores, key=confidence_scores.get)
        confidence = confidence_scores[label]

        # Calculate processing time
        start_time = datetime.now()
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # Prepare template data
        template_data = {
            'patient_name': patient_data['name'],
            'age': patient_data['age'],
            'sex': patient_data['sex'],
            'email': patient_data['email'],
            'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'processing_time': round(processing_time, 2),
            'image_path': save_path,
            'label': label.capitalize(),
            'confidence': confidence,
            'confidence_scores': confidence_scores,
            'original_image': f"uploads/{filename}",
            'processed_image': f"uploads/{processed_filename}",
            'region_data': [{'x': 100, 'y': 100, 'width': 50, 'height': 50}]  # Example region data
        }

        return render_template('result.html', **template_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)