from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

import os
from pathlib import Path
from ..core.labeling import VisionModel
from ..retrieval.upload import QdrantDB
from ..utils.constants import IMAGE_EXTENSIONS

# Initialize Flask app
app = Flask(__name__)
app.secret_key = '123'

# Configurations
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize QdrantDB and VisionModel
qdrant = QdrantDB()
vision_model = VisionModel()

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'POST':
        folder = request.files.getlist('images')  # Get all uploaded files

        uploaded_files = []
        for image in folder:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(file_path)  # Save each image to the upload folder
                uploaded_files.append(file_path)

        # Process images after saving
        if uploaded_files:
            try:
                vision_model.process_images(Path(app.config['UPLOAD_FOLDER']))
                flash('Images processed and uploaded successfully!')
            except Exception as e:
                flash(f'Error processing images: {e}')
                return redirect(request.url)
        else:
            flash('No valid images were uploaded.')
    return render_template('upload.html')

@app.route('/search', methods=['GET', 'POST'])
def search_images():
    results = None
    if request.method == 'POST':
        # Get the search query from the form
        query = request.form.get('query')

        if query:
            try:
                # Use Qdrant to search for matching captions
                results = qdrant.search(query)
            except Exception as e:
                flash(f'Error searching images: {e}')
                return redirect(request.url)
        else:
            flash('Please enter a search query.')

    return render_template('search.html', results=results)