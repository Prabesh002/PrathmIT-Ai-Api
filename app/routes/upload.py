from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from app.utils import vector_db 

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)

    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    upload_path = os.path.join(upload_folder, filename)
    file.save(upload_path)
    updated = vector_db.update_index(upload_path)
    return jsonify({'message': 'File uploaded', 'index_updated': updated}), 200