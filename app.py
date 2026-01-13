from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import time
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load the trained model
model = load_model('breast_cancer_diagnosis_model.h5')
class_labels = ['benign', 'malignant', 'normal']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(img_path, target_size=(150, 150)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def predict_cancer(img_path):
    img_array = preprocess_image(img_path)
    prediction = model.predict(img_array)
    probabilities = prediction[0]
    predicted_class_index = np.argmax(probabilities)
    predicted_class_label = class_labels[predicted_class_index]
    confidence = probabilities[predicted_class_index]
    return predicted_class_label, confidence, probabilities

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
            img = img.resize((150, 150))

            # Save processed image
            processed_filename = 'processed_{}'.format(filename)
            processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
            img.save(processed_path)

        except Exception as e:
            # If image processing fails, set defaults and continue
            processed_filename = ''
            processed_path = ''

        # Get form data with default values
        patient_data = {
            'name': request.form.get('name', ''),
            'age': request.form.get('age', ''),
            'sex': request.form.get('sex', ''),
            'email': request.form.get('email', '')
        }

        # Calculate processing time
        start_time = datetime.now()
        label, confidence, probabilities = predict_cancer(save_path)
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        confidence_scores = {
            'benign': float(probabilities[0]),
            'malignant': float(probabilities[1]),
            'normal': float(probabilities[2])
        }

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
            'original_image': "uploads/{}".format(filename),
            'processed_image': "uploads/{}".format(processed_filename),
            'region_data': [{'x': 100, 'y': 100, 'width': 50, 'height': 50}]  # Example region data
        }

        return render_template('result.html', **template_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)