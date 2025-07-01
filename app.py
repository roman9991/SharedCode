# app.py
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import os
import pydicom
from PIL import Image
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
EXPORT_FOLDER = 'exports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('dicomFiles')
    saved_files = []
    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        saved_files.append(filename)
    return jsonify({'uploaded': saved_files})

@app.route('/dicom/<filename>', methods=['GET'])
def get_dicom_metadata(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    ds = pydicom.dcmread(filepath)
    metadata = {elem.keyword: str(elem.value) for elem in ds if elem.keyword}
    return jsonify(metadata)

@app.route('/dicom/<filename>', methods=['POST'])
def update_dicom_metadata(filename):
    updates = request.json
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    ds = pydicom.dcmread(filepath)
    for key, value in updates.items():
        if hasattr(ds, key):
            setattr(ds, key, value)
    ds.save_as(filepath)
    return jsonify({'status': 'updated'})

@app.route('/export/<filename>', methods=['GET'])
def export_file(filename):
    format = request.args.get('format', 'dicom')
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if format == 'jpg':
        ds = pydicom.dcmread(filepath)
        image = Image.fromarray(ds.pixel_array).convert('L')
        output_path = os.path.join(EXPORT_FOLDER, filename + '.jpg')
        image.save(output_path)
        return send_file(output_path, mimetype='image/jpeg')
    else:
        output_path = os.path.join(EXPORT_FOLDER, filename)
        ds.save_as(output_path)
        return send_file(output_path, mimetype='application/dicom')

if __name__ == '__main__':
    app.run(debug=True)
